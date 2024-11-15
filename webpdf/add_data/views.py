from django.shortcuts import render
from django.http import HttpResponse
from app.forms import DuLieuForm

# Create your views here.
def add_data(request):
    form = DuLieuForm  
    return render(request, 'add_data/add_data.html', { 'form': form})

def get_data(request):
    if request.method == "POST":
        form = DuLieuForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("save success")
    else:
        return HttpResponse("not POST")