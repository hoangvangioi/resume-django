from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .models import Contact
from django.core.mail.message import EmailMessage


class ContactForm(forms.ModelForm):
    full_name = forms.CharField(max_length=120,
                        label=_('Full Name'),
                        required=True,
                        help_text='Write here your message!',
                        error_messages={'invalid': "A first name must start in upper case.", 'required': 'Please enter your name',
                        
                        },
                        
                        widget=forms.TextInput(
                            attrs={'data-error': "Name is required.",
                            'id': "form_name",
                            }))
    email = forms.EmailField(required=True, 
        label=_('Email Address'),
                        error_messages={'invalid': "A first name must start in upper case."},

        widget=forms.EmailInput(
                            attrs={'id': "form_email",
                            'data-error': "Valid email is required."
                            }))
    subject = forms.CharField(max_length=255,
                            label=_('Subject'),
                            required=True,
                        error_messages={'invalid': "A first name must start in upper case."},

                            widget=forms.TextInput(
                                attrs={'id': "form_subject",
                                    'data-error': "Subject is required."
                                }))
    message = forms.CharField(required=True,
        label=_('Message'),
                        error_messages={'invalid': "A first name must start in upper case."},

        widget=forms.Textarea(
            attrs={'id': "form_message",
                    'rows': "7",
                    'data-error': "Please, leave me a message."    
            }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = ''


    class Meta:
        model = Contact
        fields = '__all__'


        # labels = {
        #     'name': _('Writer'),
        # }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }

    def send_mail(self):
        full_name = self.cleaned_data['full_name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        content = f'full_name: {full_name}\nE-mail: {email}\nsubject: {subject}\nmessage: {message}'

        content += render_to_string('app/send_email.html', {
        'full_name': full_name,
        'from_email': email,
        'message': message,
        'subject': subject,
        })


        mail = EmailMessage(
            subject=subject,
            body=content,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            
            headers={'Reply-To': email}
        )
        mail.send()
