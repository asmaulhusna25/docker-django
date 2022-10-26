from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views import View
from django.shortcuts import render, redirect
from .models import Note
from .forms import NoteModelForm
#


class Index(View):
    def get(self, request):
        notes = Note.objects.all()
        form = NoteModelForm()
        return render(request, 'core/index.html', {'notes': notes, 'form': form})

    def post(self, request):
        form = NoteModelForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('notes')


class Delete(View):
    def get(self, request, pk):
        note = Note.objects.get(pk=pk)
        note.delete()
        return redirect('notes')


class Update(View):
    def get(self, request, pk):
        note = Note.objects.get(pk=pk)
        notes = Note.objects.all()
        form = NoteModelForm(instance=note)
        update_flag = True
        return render(request, 'core/index.html', {'form': form, 'notes': notes, 'update_flag': update_flag, 'note': note})

    def post(self, request, pk):
        note = Note.objects.get(pk=pk)
        print(pk)
        form = NoteModelForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
        return redirect('notes')
#


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
