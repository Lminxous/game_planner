import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from game_planner.users.schema import UserType
from django.core.exceptions import ObjectDoesNotExist
from graphql_jwt.decorators import login_required
from main import models


class Listing(DjangoObjectType):
    class Meta:
        model = models.Listing
        fields = ['id', 'organiser','game', 'group','start', 'end',] 

class Group(DjangoObjectType):
    class Meta:
        model = models.Group
        fields = ['id','game',]

class Query(graphene.ObjectType):
    all_groups = graphene.List(Group)
    group = graphene.Field(Group, game=graphene.String())
    all_listings = graphene.List(Listing)

    @login_required
    def resolve_all_groups(self, info, **kwargs):
        return models.Group.objects.all()

    @login_required
    def resolve_group(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            try:
                return models.Group.objects.get(id=id)
            except ObjectDoesNotExist:
                return None    
        return None

    @login_required
    def resolve_all_listings(self, info,**kwargs):
        return models.Listing.objects.all()

class GroupInput(graphene.InputObjectType):
    game = graphene.String()  

class ListingInput(graphene.InputObjectType):
    game = graphene.String()
    start = graphene.String()
    end = graphene.String() 
    group = graphene.Field(GroupInput)     


class CreateListing(graphene.Mutation):
    listing = graphene.Field(Listing)

    class Arguments:
       input = ListingInput(required=True)       

    @staticmethod
    def mutate(root, info,input=None):
        user = info.context.user or None
        listing = models.Listing(**input)
        listing.save()
        return CreateListing(listing=listing)
          
class Mutation(graphene.ObjectType):
    create_listing = CreateListing.Field()

# class CreateListing(graphene.Mutation):
#     listing = graphene.Field(Listing)

#     class Arguments:
#         game = graphene.String()
#         start = graphene.String()
#         end = graphene.String()        

#     def mutate(self, info,game,start,end):
#         user = info.context.user or None
#         listing = models.Listing(organiser=user,game=game,start=start,end=end)
#         listing.save()
#         return CreateListing(listing=listing)
          
# class Mutation(graphene.ObjectType):
#     create_listing = CreateListing.Field()
