from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import (About, Accounts, Blog, Certificates, Contact, Educations,
                     Experiences, Portfolios, Skills, SocialLinks)

"""Integrate with admin module."""
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

# Register your models here.

@admin.register(Contact)
class ContactAdmin(TranslatableAdmin):
    list_display = ('full_name', 'email', 'subject',)
    list_display_links = ('full_name', 'email', 'subject',)
    search_fields = ('email',)


@admin.register(Accounts)
class AccountAdmin(UserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.unregister(Group)


@admin.register(Blog)
class BlogAdmin(TranslatableAdmin):
    '''Admin View for Blog'''

    list_display = ('post',)
    search_fields = ('post',)


@admin.register(Educations)
class EducationsAdmin(TranslatableAdmin):
    '''Admin View for Educations'''

    list_display = ('school',)
    list_filter = ('school',)
    search_fields = ('school',)
    ordering = ('school',)

@admin.register(Experiences)
class ExperiencesAdmin(TranslatableAdmin):
    '''Admin View for Experiences'''

    list_display = ('workplace',)
    list_filter = ('workplace',)
    search_fields = ('workplace',)
    ordering = ('workplace',)

@admin.register(Skills)
class SkillsAdmin(TranslatableAdmin):
    '''Admin View for Skills'''

    list_display = ('skill',)
    search_fields = ('skill',)


@admin.register(Certificates)
class CertificatesAdmin(TranslatableAdmin):
    '''Admin View for Certificates'''

    list_display = ('name',)
    search_fields = ('name',)


@admin.register(About)
class AboutAdmin(TranslatableAdmin):
    '''Admin View for About'''

    list_display = ('account',)
    search_fields = ('account',)


@admin.register(Portfolios)
class PortfoliosAdmin(TranslatableAdmin):
    '''Admin View for Portfolios'''

    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    '''Admin View for SocialLinks'''

    list_display = ('account',)
    search_fields = ('account',)