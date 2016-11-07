from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class IndexView(TemplateView):
    model = Profile
    template_name = "index.html"

class GARBAGEView(View):
    def post(self, request):
        x = request.POST['code']
        y = str(x)
        for char in y:
            if char.isalpha():
                return HttpResponseRedirect("http://localhost:8000/")
        try:
            target = Child.objects.get(code=x)
        except ObjectDoesNotExist:
            return HttpResponseRedirect("http://localhost:8000/")
        return HttpResponseRedirect("http://localhost:8000/child/{}/{}".format(target.id, x))

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
        for child in kids:
            find.append(child.stay_set.all())
        total = 0
        for kid in find:
            for stay in kid:
                total += float(stay.str_dif())
        total_floor = int(total)
        minutes = int((total - total_floor) * 60)
        context['minutes'] = minutes
        context['total'] = total_floor
        context['find'] = find
        context['kids'] = kids
        context['active'] = active_parent
        return context

class ChildDetailView(DetailView):
    model = Child

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        child = Child.objects.get(id=self.kwargs['pk'])
        code = int(self.kwargs['sk'])
        if code != child.code:
            raise PermissionDenied


        stays = Stay.objects.filter(child=child.id)
        try:
            active = stays.get(active=True)
            if active:
                context['current'] = active
                context['active'] = True
        except ObjectDoesNotExist:
            context['active'] = False
        try:
            old = stays.filter(active=False).order_by('-in_time')
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

class FacultyView(LoginRequiredMixin, TemplateView):
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
    def get_success_url(self):
        return reverse('faculty_view')
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
