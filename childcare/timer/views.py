from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from timer.models import Profile, Child, Stay


class IndexView(TemplateView):
    model = Profile
    template_name = "index.html"



class GARBAGEView(View):

    def post(self, request):
        # #####
        print(request.POST)

        # #####
        return HttpResponseRedirect("/")

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"

class ProfileView(TemplateView):
    template_name = "profile.html"
    model = Profile
    def get_context_data(self):
        context = super().get_context_data()
        active_parent = Profile.objects.get(user=self.request.user)
        kids = Child.objects.filter(parent=active_parent)
        context['kids'] = kids
        context['active'] = active_parent
        return context

class ChildDetailView(DetailView):
    model = Child
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


class StayCreateView(CreateView):
    model = Stay
    success_url = "/"


    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.child = Child.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)