# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from task.models import Todo


class LoginForm(forms.Form):
    email = forms.CharField(
        label=_(u'Email'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _(u'Email'),
        })
    )
    password = forms.CharField(
        label=_(u'Password'),
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _(u'Password'),
        })
    )


class SignUpForm(forms.Form):
    first_name = forms.CharField(
        label=_(u'First Name'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control signupName',
            'placeholder': _(u'First Name'),
        })
    )
    last_name = forms.CharField(
        label=_(u'Last Name'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control signupLastName',
            'placeholder': _(u'Last Name'),
        })
    )
    email_address = forms.CharField(
        label=_(u'Email Address'),
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control signupEmail',
            'placeholder': _(u'Email Address'),
        })
    )
    password = forms.CharField(
        label=_(u'Password'),
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control signupPassword',
            'placeholder': _(u'Password'),
        })
    )
    confirm_password = forms.CharField(
        label=_(u'Confirm Password'),
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control signupPasswordConfirm',
            'placeholder': _(u'Confirm Password'),
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