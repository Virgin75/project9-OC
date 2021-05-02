from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from bookreviews.forms import TicketForm
from bookreviews.models import UserFollows
from registration.models import User
from django.contrib import messages


@login_required()
def feed(request):
    return render(request, 'bookreviews/feed.html', {'data': 'data'})


@login_required()
def follow(request):
    if request.method == 'POST':
        try:
            user_to_follow = User.objects.get(email=request.POST.get('email'))
            UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
            messages.success(request, 'Vous suivez un nouvel utilisateur.')
        except User.DoesNotExist:
            messages.error(request, "Cet utilisateur n'existe pas.")
        finally:
            return redirect('follow_view')

    if request.method == 'GET':
        i_follow = UserFollows.objects.filter(user=request.user)
        my_followers = UserFollows.objects.filter(followed_user=request.user)

        autocomplete = User.objects.exclude(
            Q(email__in=[usr.followed_user for usr in i_follow]) |
            Q(email=request.user.email))

        return render(request, 'bookreviews/follow.html', {'i_follow': i_follow, 'my_followers': my_followers, 'all_users': autocomplete})


@login_required()
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            messages.success(request, 'Ticket créé avec succès.')
            return redirect('feed_view')

    if request.method == 'GET':
        form = TicketForm()
    return render(request, 'bookreviews/create-ticket.html', {'form': form})


@login_required()
def create_review(request):
    pass


@login_required()
def edit_own_ticket(request, ticket_id):
    pass


@login_required()
def edit_own_review(request, review_id):
    pass


@login_required()
def my_posts(request):
    pass
