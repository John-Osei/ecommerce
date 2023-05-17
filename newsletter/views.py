from django.shortcuts import render
from .forms import SubscribersForm
# Create your views here.


def index(request):
    if request.method == 'POST':
        form = SubscribersForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SubscribersForm()
    form = SubscribersForm()

    context ={
        'form': form,
    }
    return render(request, 'core/index.html', context)