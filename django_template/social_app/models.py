from django.db import models
from django.contrib.auth.models import User


# Ein Spieler besitzt einen Namen, ein Passwort und Erfahrung. Diese wird auf CLientseite in das Level umgerechnet
class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    experience = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


# This represents a 2-4 player match
class Match(models.Model):
    # The host is mostly used as an identifier so that players can find the
    # match they have hosted or joined.
    host = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
    )
    # Boolsche-Werte, die anzeigen, ob das Spiel bereits gestartet hat oder vorbei ist
    has_started = models.BooleanField(default=False)
    is_over = models.BooleanField(default=False)
    number_of_players = models.IntegerField(default=0)
    # Die Koordinaten des Geistes
    position_ghost_x = models.DecimalField(default=0, max_digits=30, decimal_places=20)
    position_ghost_z = models.DecimalField(default=0, max_digits=30, decimal_places=20)


# TODO: Anpassen, und in Gruppe statt Freundschaft umändern
class Friendship(models.Model):
    # Because both these foreign keys are players, they need to be
    # distinguished using related_name. This way, the list of a player's
    # friends is unique and different from the list of a player's followers.
    # Followers are players who have befriended you, while friends are players
    # who you have befriended.
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='friends',
    )
    friend = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='followers',
    )
    level = models.IntegerField(default=0)

    # The addition of this class ensures that 2 players cannot befriend each
    # other more than once, but it is still possible for a player to
    # befriend any number of different players and for that player to be
    # befriended by any number of different players. If you prefer
    # friendships always being symmetric, i.e. if player A is the friend
    # of player B, player B is automatically the friend of player A,
    # this can also be done.
    class Meta:
        unique_together = ('player', 'friend')

    # These str methods are mostly used for debugging purposes. The
    # admin page of the site also uses this str method to display that
    # particular model.
    def __str__(self):
        return f'{self.player.user.username} -> {self.friend.user.username}'
