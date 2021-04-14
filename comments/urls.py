from django.urls import path
from . import views

urlpatterns = [
    path('add-comment/', views.comment_add, name='add_comment'),
    path('<int:comment_id>/comment-delete/', views.comment_delete,
         name='delete_comment'),
]
