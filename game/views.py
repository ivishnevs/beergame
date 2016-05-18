from django.shortcuts import render
from game.forms import CreateGameForm
from django.contrib.auth.models import User
from game.models import Game, Gamer
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def my_game_list(request):
    my_game_list = request.user.game_set.all()

    return render(request, 'game/my_game_list.html', {'my_game_list': my_game_list})


def edit_game(request, pk):
    game = Game.objects.get(pk=pk) if pk else None
    if request.method == 'POST':
        cgf = CreateGameForm(request.POST, instance=game)
        if cgf.is_valid():
            game = cgf.save(commit=False)
            game.user = request.user
            game.save()
            game.create_gamers()
    else:
        cgf = CreateGameForm(instance=game)

    return render(request, 'game/edit_game.html', {'form': cgf})


def game_list(request):
    users = User.objects.all()
    users_with_game_set = []
    for user in users:
        if user.game_set:
            users_with_game_set.append(user)

    return render(request, 'game/game_list.html', {'users_with_game_set': users_with_game_set})


def choose_role(request, pk):
    game = Game.objects.get(pk=pk)
    gamers = game.gamer_set.filter(active=False)

    return render(request, 'game/choose_role.html', {'gamers': gamers})


def game(request, pk):
    gamer = Gamer.objects.get(pk=pk)
    if request.method == 'POST':
        order = int(request.POST['order'])
        gamer.make_order(order)
        gamer.record_stats()
        gamer.make_supply()
        gamer.complete_step()

        return HttpResponseRedirect(reverse('game', args=[pk]))

    return render(request, 'game/game.html', {'gamer': gamer})


def game_stat(request, pk):
    game = Game.objects.get(pk=pk)
    gamers = game.gamer_set.all()
    stat_sets = []
    for gamer in gamers:
        stat_sets.append(gamer.stats_set)
