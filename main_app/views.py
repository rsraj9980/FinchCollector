from django.db.models import fields
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch
# Create your views here.
from .forms import FeedingForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finchs_index(request):
  finchs = Finch.objects.all()
  return render(request, 'finchs/index.html', {'finchs': finchs})


def finchs_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()
  return render(request, 'finchs/detail.html', {
    'finch': finch, 'feeding_form': feeding_form
  })

class FinchCreate(CreateView):
  model = Finch
  fields = '__all__' 
  success_url = '/finchs/'

class FinchUpdate(UpdateView):
  model = Finch
  fields = ['breed', 'description', 'age']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finchs/'

def add_feeding(request, finch_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the finch_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)