from django.urls import path

from . import views

# More complex URL-patterns can be found in the Django documentation,
# but since these URLs will be accessed by the client automatically rather
# than a user, they can be kept very straightforward.
urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.signin),
    path('logout/', views.signout),
    path('check_auth/', views.check_auth),
    path('get_experience/', views.get_experience),
    path('edit_experience/', views.edit_experience),
    path('get_names/', views.get_names),
    path('add_friend/', views.add_friend),
    path('host_match/', views.host_match),
    path('join_match/', views.join_match),
    path('end_match/', views.end_match),
    path('start_match/', views.start_match),
]
