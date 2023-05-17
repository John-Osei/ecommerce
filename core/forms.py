from django import forms
from core.models import ProductReview
from tinymce.widgets import TinyMCE


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write review'}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']

class NewsletterForm(forms.Form):
    subject = forms.CharField(max_length=100)
    receivers = forms.CharField()
    message = forms.CharField(widget=TinyMCE(), label="Email content")
