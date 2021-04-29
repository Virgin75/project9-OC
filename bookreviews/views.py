from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required()
def feed(request):
    return render(request, 'bookreviews/feed.html', {'data': 'data'})


@login_required()
def follow(request):
    pass


@login_required()
def create_ticket(request):
    pass


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
