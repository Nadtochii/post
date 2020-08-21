from django.urls import path

from . import views

urlpatterns = [
    path('', views.ItemList.as_view(), name='item-list'),
    path('add/', views.ItemCreate.as_view(), name='item-add'),
    path('<int:pk>/', views.ItemDetail.as_view(), name='item-detail'),
    path('<int:pk>/delete/', views.ItemDelete.as_view(), name='item-delete'),
    path('<int:pk>/comment/', views.CommentCreate.as_view(), name='comment-add'),
    # path('<int:pk>/comment/<int:pk>/>delete/', views.CommentDelete.as_view(), name='comment-delete'),
]

