from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from timer.models import Profile, Child, Stay
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta, timezone
from django.utils import timezone
import random



class IndexView(TemplateView):
    model = Profile
    template_name = "index.html"

class GARBAGEView(View):

    def post(self, request):
        # #####
        print(request.POST)
        x = request.POST['code']
        target = Child.objects.get(code=x)


        # #####
        return HttpResponseRedirect("http://localhost:8000/child/{}/".format(target.id))

class NEWView(View):
    template_name = 'new_view.html'


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
        find = []
        # for kid in kids:
        #     find.append(Stay.objects.filter(child=kid))
        # for x in find[0]:
        #     print(x.id)
        for child in kids:
            find.append(child.stay_set.all())
        context['find'] = find
        context['kids'] = kids
        context['active'] = active_parent
        return context

class ChildDetailView(DetailView):
    model = Child
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        child = Child.objects.get(id=self.kwargs['pk'])
        stays = Stay.objects.filter(child=child.id)
        try:
            active = stays.get(active=True)
            if active:
                context['current'] = active
                context['active'] = True
        except ObjectDoesNotExist:
            context['active'] = False
        try:
            old = stays.filter(active=False)
            context['old'] = old
        except ObjectDoesNotExist:
            pass

        return context


class StayCreateView(CreateView):
    model = Stay
    success_url = "/"
    fields = ("notes", )

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.child = Child.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

class StayUpdateView(UpdateView):
    model = Stay
    success_url = "/"
    fields = []

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.active = False
        instance.out_time = datetime.now
        return super().form_valid(form)

class FacultyView(TemplateView):
    model = Profile
    template_name = "faculty.html"

    def get_context_data(self):
        context = super().get_context_data()
        profiles = Profile.objects.filter(profile_type="p")
        kids = Child.objects.all()
        active = Stay.objects.filter(active=True)
        context['profiles'] = profiles
        context['kids'] = kids
        context['active'] = active
        return context

class ChildCreateView(CreateView):
    model = Child
    success_url = "/"
    fields = ('first_name', 'last_name', 'parent')


    def coder(self):
        x = []
        for step in range(4):
            x.append(str(random.randint(0,9)))
        return int("".join(x))


    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.code = self.coder()
        return super().form_valid(form)
