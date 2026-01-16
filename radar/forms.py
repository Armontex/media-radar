from django import forms
from .choices import NotifyChannelChoices


class EmailForm(forms.Form):
    email = forms.EmailField(label="Email")


class NotifyChannelForm(forms.Form):
    channel = forms.ChoiceField(choices=NotifyChannelChoices.choices, label="notify channel",
                                widget=forms.Select(attrs={"onchange": "this.form.submit();"}))
