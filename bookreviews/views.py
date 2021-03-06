from django.shortcuts import render, redirect
from django.db.models import Q, CharField, Value
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from bookreviews.forms import TicketForm, ReviewForm
from bookreviews.models import UserFollows, Ticket, Review
from registration.models import User

from itertools import chain


@login_required()
def feed(request):
    i_follow = UserFollows.objects.filter(
        user=request.user).values_list('followed_user')

    ticket_list = Ticket.objects.filter(
        Q(user__in=[usr for usr in i_follow]) |
        Q(user=request.user)
    ).annotate(content_type=Value('TICKET', CharField()))

    review_list = Review.objects.filter(
        Q(user__in=[usr for usr in i_follow]) |
        Q(user=request.user)
    ).annotate(content_type=Value('REVIEW', CharField()))

    posts = sorted(
        chain(review_list, ticket_list),
        key=lambda post: post.time_created,
        reverse=True
    )

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    paginated_posts = paginator.get_page(page)

    return render(
        request,
        'bookreviews/feed.html',
        context={'posts': paginated_posts, 'user': request.user}
    )


@login_required()
def follow(request):
    if request.method == 'POST':
        try:
            user_to_follow = User.objects.get(email=request.POST.get('email'))
            UserFollows.objects.create(
                user=request.user,
                followed_user=user_to_follow
            )
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

        return render(
            request,
            'bookreviews/follow.html',
            {'i_follow': i_follow,
             'my_followers': my_followers,
             'all_users': autocomplete}
        )


@login_required()
def unfollow(request, user_id):
    user_to_unfollow = User.objects.get(id=user_id)
    UserFollows.objects.get(followed_user=user_to_unfollow, user=request.user).delete()
    messages.success(request, 'D??sabonnement r??alis?? avec succ??s.')
    return redirect('follow_view')


@login_required()
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            messages.success(request, 'Ticket cr???? avec succ??s.')
            return redirect('feed_view')

    if request.method == 'GET':
        form = TicketForm()
    return render(
        request,
        'bookreviews/create-ticket.html',
        {'form': form}
    )


@login_required()
def create_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            # Cr??ation du ticket
            ticket_form_data = ticket_form.save(commit=False)
            ticket_form_data.user = request.user
            ticket_form_data.save()
            messages.success(request, 'Ticket cr???? avec succ??s.')
            # Cr??ation de la review associ??e
            review_form_data = review_form.save(commit=False)
            review_form_data.user = request.user
            review_form_data.ticket = Ticket.objects.get(
                id=ticket_form_data.id)
            review_form_data.save()
            messages.success(request, 'Review cr????e avec succ??s.')
            return redirect('feed_view')

    if request.method == 'GET':
        ticket_form = TicketForm()
        review_form = ReviewForm()
    return render(
        request,
        'bookreviews/create-review.html',
        {'review_form': review_form, 'ticket_form': ticket_form})


@login_required()
def create_review_from_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            # Cr??ation de la review associ??e
            review_form_data = review_form.save(commit=False)
            review_form_data.user = request.user
            review_form_data.ticket = ticket
            review_form_data.save()
            messages.success(request, 'Review cr????e avec succ??s.')
            return redirect('feed_view')

    if request.method == 'GET':
        review_form = ReviewForm()
    return render(
        request,
        'bookreviews/create-review-from-ticket.html',
        {'review_form': review_form, 'ticket': ticket, 'user': request.user})


@ login_required()
def edit_own_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if ticket.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket modifi?? avec succ??s.')
            return redirect('my_posts_view')

    if request.method == 'GET':
        form = TicketForm(instance=ticket)
        return render(
            request,
            'bookreviews/edit-ticket.html',
            {'form': form, 'ticket_id': ticket_id})


@ login_required()
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if ticket.user != request.user:
        return HttpResponseForbidden()

    ticket.delete()

    messages.success(request, 'Ticket supprim?? avec succ??s.')
    return redirect('my_posts_view')


@ login_required()
def edit_own_review(request, review_id):
    review = Review.objects.get(id=review_id)

    if review.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review modifi??e avec succ??s.')
            return redirect('my_posts_view')
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(
            request,
            'bookreviews/edit-review.html',
            {'form': form, 'review_id': review_id, 'ticket': review.ticket})


@ login_required()
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)

    if review.user != request.user:
        return HttpResponseForbidden()

    review.delete()

    messages.success(request, 'Review supprim??e avec succ??s.')
    return redirect('my_posts_view')


@ login_required()
def my_posts(request):
    ticket_list = Ticket.objects.filter(
        user=request.user
    ).annotate(content_type=Value('TICKET', CharField()))

    review_list = Review.objects.filter(
        user=request.user
    ).annotate(content_type=Value('REVIEW', CharField()))

    posts = sorted(
        chain(review_list, ticket_list),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(
        request,
        'bookreviews/my-posts.html',
        context={'posts': posts})
