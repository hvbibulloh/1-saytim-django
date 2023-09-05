from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views import View

from .forms import LoginForm, UserRegistrationForm, UserEdit, ProfileEdit
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Profile


def user_login(request):
    if request == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Fine Welcome !!!')
                else:
                    return HttpResponse('Sizning profilingiz faol holatda emas')

            else:
                return HttpResponse('Error profile !!! ')

    else:
        form = LoginForm()


    return render(request, 'registration/login.html', {'form':form})


@login_required()
def dashboard_view(request):
    user = request.user
    profile_info = Profile.objects.get(user=user)
    context = {
        'user':user,
        'profile': profile_info
    }

    return render(request, 'pages/user_profile.html', context)



def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user" : new_user
            }
            return render(request, 'accaunt/register_done.html', context)

    else:
        user_form = UserRegistrationForm()
        context = {
            "user_form": user_form
        }
        return render(request, 'accaunt/register.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accaunt/register.html'

@login_required
def edit_user(request):
    if request.method =="POST":
        user_form = UserEdit(instance=request.user, data=request.POST)
        profile_form = ProfileEdit(instance=request.user.profile,
                                   data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

    else:
        user_form = UserEdit(instance=request.user)
        profile_form = ProfileEdit(instance=request.user.profile)

    return render(request, 'accaunt/profile_edit.html', {'user_form':user_form, 'profile_form':profile_form})




#class uchun edit_user

class EditUserView(LoginRequiredMixin,View):
    def get(self, request):
        user_form = UserEdit(instance=request.user)
        profile_form = ProfileEdit(instance=request.user.profile)

        return render(request, 'accaunt/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        if request.method == "POST":
            user_form = UserEdit(instance=request.user, data=request.POST)
            profile_form = ProfileEdit(instance=request.user.profile,
                                       data=request.POST, files=request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('user_profile')

