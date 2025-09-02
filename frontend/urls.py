from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signup/', views.signup.as_view(), name='signup'),
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout.as_view(), name='logout'),
    path('profile/', views.profile.as_view(), name='profile'),
    path('profile-update/', views.profile_update.as_view(), name='profile_update'),
    path('add-complaint/', views.add_complaint.as_view(), name='add_complaint'),
    path('vote-complaint/', views.vote_complaint.as_view(), name='vote_complaint'),
    path('complaint-records/', views.complaint_records.as_view(), name='complaint_records'),
    path('complaint/<slug:slug>/', views.complaint.as_view(), name='complaint'),
    path('take-complaint/', views.take_complaint.as_view(), name='take_complaint'),
    path('update-complaint-status/', views.update_complaint_status.as_view(), name='update_complaint_status'),
    path('how-it-works/', views.how_it_works.as_view(), name='how_it_works'),
]
