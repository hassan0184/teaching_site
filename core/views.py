from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .models import Service, Contact
from django.http import HttpResponseRedirect                                     
from .forms import ContactForm 
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .forms import BookingForm
from django.shortcuts import render
from django.conf import settings


import paypalrestsdk
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def create_payment(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        price = request.POST.get('price')
        description = request.POST.get('description')
        currency = request.POST.get('currency')
        print(price,service_id,currency)

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('payment_execute')),
                "cancel_url": request.build_absolute_uri(reverse('payment_cancel'))
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": description,
                        "sku": service_id,
                        "price": price,
                        "currency": currency,
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": price,
                    "currency": currency
                },
                "description": description
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    redirect_url = str(link.href)
                    return JsonResponse({"redirect_url": redirect_url})
        else:
            return JsonResponse({"error": payment.error})
    return JsonResponse({"error": "Invalid request method"})

def payment_execute(request):
    payer_id = request.GET.get('PayerID')
    payment_id = request.GET.get('paymentId')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Payment execution successful
        messages.success(request, 'Your payment was successful. Thank you for your purchase!')
        return redirect(reverse('home'))  # Redirect to the home page
    else:
        # Payment execution failed
        messages.error(request, f'Payment error: {payment.error}')
        return redirect(reverse('home'))  # Redirect to the home page


def payment_cancel(request):
    return render(request, 'payment_error.html')



# def process_payment(request):
#     print(settings.PAYPAL_CLIENT_ID)
#     print(settings.PAYPAL_SECRET_KEY)

#     if request.method == 'POST':
#         service_id = request.POST.get('service_id')
#         price = request.POST.get('price')
#         description = request.POST.get('description')
#         currency = request.POST.get('currency')

#         paypal_payment = Payment({
#             "intent": "sale",
#             "payer": {"payment_method": "paypal"},
#             "transactions": [{
#                 "amount": {"total": price, "currency": currency},
#                 "description": description
#             }],
#             "redirect_urls": {
#                 "return_url": "http://localhost:8000/payment/execute/",
#                 "cancel_url": "http://localhost:8000/payment/cancel/"
#             }
#         })

#         if paypal_payment.create():
#             for link in paypal_payment.links:
#                 if link.method == "REDIRECT":
#                     redirect_url = str(link.href)
#                     return redirect(redirect_url)
#         else:
#             return render(request, 'payment_error.html')

#     return render(request, 'payment_error.html')

class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Camila's Site"
        context['services'] = Service.objects.all()
        return context

def save_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for contacting us. We will get back to you soon.'  )
            return redirect(reverse('home'))
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def save_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Booking successful!'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)