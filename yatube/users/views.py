from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import CreationForm, ExpansionCreationForm

User = get_user_model()


class SignUp(CreateView):
    template_name = 'users/signup.html'
    model = User
    form_class = CreationForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        expansion_creation_form = ExpansionCreationForm()
        return self.render_to_response(
            self.get_context_data(
                form=form, expansion_creation_form=expansion_creation_form
            ))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        expansion_creation_form = ExpansionCreationForm(self.request.POST)
        if form.is_valid() and expansion_creation_form.is_valid():
            return self.form_valid(form, expansion_creation_form)
        else:
            return self.form_invalid(form, expansion_creation_form)

    def form_valid(self, form, expansion_creation_form):
        user = form.save()
        cleaned_data = expansion_creation_form.cleaned_data[0]
        user.profile.tel = cleaned_data['tel']
        user.profile.location = cleaned_data['location']
        user.profile.birth_date = cleaned_data['birth_date']
        # user.save() login заменяет save
        login(self.request, user)
        return redirect('posts:index')

    def form_invalid(self, form, expansion_creation_form):
        return self.render_to_response(
            self.get_context_data(
                form=form, expansion_creation_form=expansion_creation_form
            ))
