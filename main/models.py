from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from .utils import find_overlap_range,find_max_overlap_range


GAME_CHOICES = (
    ("PUBG", "PlayerUnknown's Battlegrounds"),
    ("CSGO", "Counter-Strike: Global Offensive"),
    ("GTAV", "Grand Theft Auto V"),
    ("VALR", "Valorant"),
    ("RAIN", "Rainbow Six Siege"),
)

class Listing(models.Model):
    player = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    group = models.ForeignKey(
        "Group", related_name="members", on_delete=models.CASCADE, null=True, blank=True
    )
    game = models.CharField(choices=GAME_CHOICES, max_length=4)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def to_dict(self):
        if self.group is None:
            group_info = None
        else :
            group_info = self.group.pk
        return {
            "pk": self.pk,
            "player": self.player.pk,
            "group": group_info,
            "game": self.game,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
        }

    def __str__(self):
        return f"Listing({self.player}, {self.game})"

class GroupManager(models.Manager):
    def groups_by_game(self, game):
        return self.filter(game=game)        

class Group(models.Model):

    MAX_MEMBERS = 4

    game = models.CharField(choices=GAME_CHOICES, max_length=4)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_full = models.BooleanField(default=False)

    objects = GroupManager()

    def save(self):
        if self.members.count() == self.MAX_MEMBERS:
            self.is_full = True
        super().save()

    def to_dict(self):
        return {
            "pk": self.pk,
            "game": self.game,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "members": [m.to_dict() for m in self.members.all()],
            "is_full": self.is_full,
        }

    def __str__(self):
        return f"Group({self.game})"  

    class Meta:
        verbose_name_plural = "Groups"          