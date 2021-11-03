from django.db.models import fields
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Toy
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
  # Get the toys the cat doesn't have
  toys_finch_doesnt_have = Toy.objects.exclude(id__in=finch.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'finchs/detail.html', {
    'finch': finch, 'feeding_form': feeding_form,
    # Add the toys to be displayed
    'toys': toys_finch_doesnt_have
  })

class FinchCreate(CreateView):
  model = Finch
  fields = ['name', 'breed', 'description', 'age']

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

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def assoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)