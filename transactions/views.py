from django.shortcuts import render
from .forms import PaymentForm

# Create your views here.

def index(request):
    form = PaymentForm()
    return render(request, 'index.html', {'form': form})


