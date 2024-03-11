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
            return JsonResponse({'message': 'Thanks for contacting us. We will get back to you soon.'})
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