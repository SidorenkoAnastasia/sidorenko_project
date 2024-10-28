from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import delete_race

urlpatterns = [
    path('', views.race_list, name='race_list'),
    path('create/', views.create_race, name='create_race'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('races/register/<int:race_id>/', views.register_for_race, name='register_for_race'),
    path('races/<int:race_id>/', views.race_detail, name='race_detail'),
    path('races/<int:race_id>/comment/', views.add_comment, name='add_comment'),
    path('races/<int:race_id>/unregister/', views.unregister_from_race, name='unregister_from_race'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('race/delete/<int:race_id>/', delete_race, name='delete_race'),
]