from django import forms
from django.forms import ModelForm
from .models import Post, SubUser, Category
from django import forms


class NewPostForm(forms.Form):
    title=forms.CharField(label='Enter a  title', label_suffix=" : ", min_length=1, max_length=30,
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           help_text="Enter your title",
                           error_messages={'required': "Enter your title"}, disabled=False, strip=True)
    text = forms.CharField(label='Enter your Post', label_suffix=" : ", min_length=1, max_length=1000,
                           required=True,
                           widget=forms.Textarea(attrs={'class': 'form-control'}),
                           help_text="Enter your Post",
                           error_messages={'required': "Enter your Post"}, disabled=False, strip=True)

    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class NewAnswerForm(forms.Form):
    text = forms.CharField(label='Enter your Answer', label_suffix=" : ", min_length=1, max_length=1000,
                           required=True,
                           widget=forms.Textarea(attrs={'class': 'form-control'}))



class user_subscription_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user=args[0]['user']
        categories=args[0]['category']
        for category in categories.objects.all():
            fieldname='category_'+str(category.id)
            if not fieldname in self.fields:
                self.fields[fieldname] = forms.BooleanField(required=False, label=category.name)
                if category.is_subscribed_by_user(user).exists():
                    self.data[fieldname]='on'
