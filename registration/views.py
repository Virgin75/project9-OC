from django.contrib.auth import login, logout, authenticate
from registration.forms import RegisterForm, SignInForm
from django.shortcuts import render, redirect


def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            return redirect('/app/feed/')

    # GET request on .../signup/
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})


def signin_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/app/feed/')

    # GET request on .../signin/
    else:
        form = SignInForm()
    return render(request, 'registration/signin.html', {'form': form})


def logout_view(request):
    logout(request)

    return redirect('signin_view')
