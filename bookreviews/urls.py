from django.urls import path

from . import views


urlpatterns = [
    path('feed/', views.feed, name='feed_view'),
    path('follow/', views.follow, name='follow_view'),
    path('unfollow/<int:user_id>', views.unfollow, name='unfollow_view'),
    path('create-ticket/', views.create_ticket, name='create_ticket_view'),
    path('ticket/<int:ticket_id>', views.edit_own_ticket, name='edit_own_ticket_view'),
    path('ticket/<int:ticket_id>/delete', views.delete_ticket, name='delete_ticket_view'),
    path('create-review-from-ticket<int:ticket_id>', views.create_review_from_ticket, name='create_review_from_ticket_view'),
    path('create-review/', views.create_review, name='create_review_view'),
    path('review/<int:review_id>', views.edit_own_review, name='edit_own_review_view'),
    path('review/<int:review_id>/delete', views.delete_review, name='delete_review_view'),
    path('my-posts/', views.my_posts, name='my_posts_view'),
]
