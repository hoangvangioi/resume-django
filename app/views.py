from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ContactForm
from .models import (Accounts, Blog, Certificates, Contact, Educations, Experiences,
                     About, Portfolios, Skills, SocialLinks)

# Create your views here.


class IndexView(FormView):
    template_name = 'index.html'
    form_class = ContactForm
    success_url = reverse_lazy('page')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['accounts'] = Accounts.objects.order_by('?').all()[:1]
        context['contact'] = Contact.objects.order_by('?').all()
        context['about'] = About.objects.order_by('?').all()[:1]
        context['social_links'] = SocialLinks.objects.order_by('?').all()[:1]
        context['educations'] = Educations.objects.order_by('?').all()
        context['skills'] = Skills.objects.order_by('?').all()
        context['experiences'] = Experiences.objects.order_by('?').all()
        context['certificates'] = Certificates.objects.order_by('?').all()
        context['portfolios'] = Portfolios.objects.order_by('?').all()
        context['posts'] = Blog.objects.order_by('?').all()   
        return context

    def form_valid(self, request, form, *args, **kwargs):
        form.send_mail()
        form.save()
        messages.success(request, 'Email was sent successfully!')
        return super(IndexView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, request, form, *args, **kwargs):
        messages.error(request, 'Error processing emails, please try again!')
        return super(IndexView, self).form_invalid(form, *args, **kwargs)