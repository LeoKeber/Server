from django.http import HttpResponse

from .models import Player, Friendship, Match
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import logout


# If this file becomes too large it is recommended to split it up into
# multiple files. This file is not special, just make sure that the correct
# file and view function is linked to the correct URL in urls.py.


# USER AUTHENTICATION: check_auth, signout, signin, signup

def check_auth(request):
    if request.user.is_authenticated:
        return HttpResponse(f'0: "{request.user.username}" is authenticated')
    else:
        return HttpResponse('1: user is not authenticated')


def signout(request):
    logout(request)
    return HttpResponse('0: successful logout')


def signin(request):
    if request.user.is_authenticated:
        return HttpResponse(f'1: "{request.user.username}" already signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    username = request.POST['username']
    password = request.POST['password']

    # authenticate() only returns a user if username and password are correct
    user = authenticate(request, username=username, password=password)
    if user is None:
        return HttpResponse(f'could not authenticate.')
    login(request, user)
    return HttpResponse('0: successful signin')


def signup(request):
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    # Instead of checking for the form data ourselves, we use the already
    # existing UserCreationForm.
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        return HttpResponse(f'invalid form: {form}')
    # This creates a user from that form
    form.save()
    # This logs in that user
    username = form.cleaned_data.get('username')
    raw_password = form.cleaned_data.get('password1')
    # We don't have to check if the username and password are correct
    # because we just created that exact user.
    user = authenticate(username=username, password=raw_password)
    login(request, user)
    # Create the user's player
    player = Player(user=user)
    # Don't forget to save at the end of all the changes to table contents
    player.save()
    return HttpResponse('0: successful signup')


# TODO: Hier kommen Gruppenlevel und Freunde:

def get_names(request):
    #if not request.user.is_authenticated:
    #    return HttpResponse(f'user not signed in')
    response = '0:'
    # Iterate through all players
    for player in Player.objects.all():
        response += f' {player.user.username}'
    return HttpResponse(response)


def add_friend(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player = request.user.player
    name = request.POST['name']
    # Keyword attributes are very powerful. Look at the Django documentation
    # for more details. This line fetches the player that has a user that
    # has a username that equals name. The __ is equivalent to a dot.
    # user.username in regular code becomes the user__username parameter of
    # the get function.
    friend = Player.objects.get(user__username=name)

    # This line creates that friendship and immediately saves it
    Friendship(player=player, friend=friend).save()

    response = f'0: {request.user.username} befriended {name}'
    return HttpResponse(response)


# TODO: Gruppenlevel und XP

# LEADERBOARD: get_scores, edit_score

def get_experience(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    response = '0: '
    # Iterates over all players
    for player in Player.objects.all():
        # Remember you can't do player.username because the player does not
        # have a username, only the player's user.
        response += f'{player.user.username} {player.experience},'
    # Removes the trailing comma left by the above iteration
    response = response[:-1]
    return HttpResponse(response)


def edit_experience(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not signed in')
    if request.method != 'POST':
        return HttpResponse('incorrect request method')
    # Get the score
    xp = request.POST['xp']
    # Change the player's score
    request.user.player.experience = int(xp)
    # Save that change
    request.user.player.save()
    response = f'0: changed the score of {request.user.username} to {xp}'
    return HttpResponse(response)



def host_match(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player = request.user.player
    if hasattr(player, 'match'):
        # The player has at some point hosted a match, so this is reset to
        # its initial state.
        player.match.host_has_ball = False
        player.match.has_started = False
        player.match.is_over = False
        player.match.position = 0
        player.match.save()
        return HttpResponse(f'0: reset match')
    else:
        # The player has never hosted a match, so the default values of the
        # newly created match are already correct.
        match = Match(host=player)
        match.save()
        return HttpResponse(f'0: created match')


def join_match(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')

    host_name = request.POST['host']
    host = Player.objects.get(user__username=host_name)
    if hasattr(host, 'match'):
        host.number_of_players += 1
        host.match.has_started = True
        host.match.save()
        return HttpResponse(f'0: joined match, started match')
    else:
        return HttpResponse(f'no match with host {host_name} exists')


def start_match(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    host_name = request.POST['host']
    host = Player.objects.get(user__username=host_name)
    if hasattr(host, 'match'):
        if host.number_of_players >= 2:
            host.match.has_started = True
        host.match.save()
        return HttpResponse(f'0: started match')
    else:
        return HttpResponse(f'no match with host {host_name} exists')


def end_match(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    host_name = request.POST['host']
    host = Player.objects.get(user__username=host_name)
    if not hasattr(host, 'match'):
        return HttpResponse(f'no match with host {host_name} exists')
    host.match.is_over = True
    host.match.save()
    return HttpResponse(f'0: ended match')
