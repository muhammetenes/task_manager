# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from task.models import Todo


class LoginForm(forms.Form):
    email = forms.CharField(
        label=_('Email'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email'),
        })
    )
    password = forms.CharField(
        label=_('Password'),
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Password'),
        })
    )


class SignUpForm(forms.Form):
    first_name = forms.CharField(
        label=_('First Name'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control signupName',
            'placeholder': _('First Name'),
        })
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control signupLastName',
            'placeholder': _('Last Name'),
        })
    )
    email_address = forms.CharField(
        label=_('Email Address'),
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control signupEmail',
            'placeholder': _('Email Address'),
        })
    )
    password = forms.CharField(
        label=_('Password'),
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control signupPassword',
            'placeholder': _('Password'),
        })
    )
    confirm_password = forms.CharField(
        label=_('Confirm Password'),
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control signupPasswordConfirm',
            'placeholder': _('Confirm Password'),
        })
    )


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['text']
        labels = {
            'text': _('Todo')
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'})
        }