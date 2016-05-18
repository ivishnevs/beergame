from django.conf.urls import url, include
from game import views

urlpatterns = [
    url(r'^$', views.game_list, name='game_list'),
    url(r'^choose-role/(?P<pk>[0-9]+)', views.choose_role, name='choose_role'),
    url(r'^edit-game/(?P<pk>[0-9]*)', views.edit_game, name='edit_game'),
    url(r'^game/(?P<pk>[0-9]+)', views.game, name='game'),
    url(r'^my-game-list', views.my_game_list, name='my_game_list')
]
