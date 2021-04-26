from django.contrib.auth import login, authenticate
from registration.forms import RegisterForm, SignInForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)

    # GET request on .../signup/
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("/logged-in")

        else:
            return redirect("/user-not-exitste")

    # GET request on .../signin/
    else:
        form = SignInForm()
    return render(request, 'registration/signin.html', {'form': form})
