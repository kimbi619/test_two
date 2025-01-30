from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from .models import Person
from django import forms


class PersonListView(ListView):

    model = Person

    template_name = 'core/person_list.html'
    
    context_object_name = 'persons'
