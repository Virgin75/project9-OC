from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from bookreviews.forms import TicketForm, ReviewForm
from bookreviews.models import UserFollows, Ticket
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
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            # Création du ticket
            ticket_form_data = ticket_form.save(commit=False)
            ticket_form_data.user = request.user
            ticket_form_data.save()
            messages.success(request, 'Ticket créé avec succès.')
            # Création de la review associée
            review_form_data = review_form.save(commit=False)
            review_form_data.user = request.user
            review_form_data.ticket = Ticket.objects.get(id=ticket_form_data.id)
            review_form_data.save()
            messages.success(request, 'Review créée avec succès.')
            return redirect('feed_view')

    if request.method == 'GET':
        ticket_form = TicketForm()
        review_form = ReviewForm()
    return render(request, 'bookreviews/create-review.html', {'review_form': review_form, 'ticket_form': ticket_form})


@login_required()
def edit_own_ticket(request, ticket_id):
    pass


@login_required()
def edit_own_review(request, review_id):
    pass


@login_required()
def my_posts(request):
    pass
