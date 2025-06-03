from django import forms

class PaymentForm(forms.Form):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'placeholder': 'Enter amount'
        }))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'placeholder': 'Enter phone number'
    }))