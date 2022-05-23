from django import forms


class CsrfOnlyForm(forms.Form):
    """CSRFProtection form, intentionally left blank"""
