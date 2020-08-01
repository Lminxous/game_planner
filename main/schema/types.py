import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from main.models import Listing
from .models import Listing,GroupManager,Group
from game_planner.users.schema import UserType



class Listing(DjangoObjectType):
    class Meta:
        model = models.Product
        fields = [
            'id', 
            'organiser',
            'game', 
            'group',
            'start', 
            'end', 
            ] 


class Group(DjangoObjectType):
    class Meta:
        model = Group
        fields = ['game']

    groups = graphene.List(Group)
    
    @staticmethod
    def resolve_groups(self, info, **kwargs):
        return self.groups.all()
