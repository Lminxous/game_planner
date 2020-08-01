import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphql_jwt.decorators import login_required
from main import models
from main.schema.types import (Listing,Group)
from game_planner.users.schema import UserType

#1 - The data the server can send back to the client
class CreateListing(graphene.Mutation):
    id = graphene.ID()
    game = graphene.String()
    start = graphene.String()
    end = graphene.String()

    #2 - The data you can send to the server
    class Arguments:
        game = graphene.String()
        start = graphene.String()
        end = graphene.String()
    #3 - Creates a listing in the database using the data sent 
    #by the user,through the url and description parameters
    def mutate(self, info, game,start,end):
        user = info.context.organiser or None
        if user.is_anonymous:
            #1
            raise GraphQLError('You must be logged in to create a Listing!')

        listing = Listing.objects.filter(id=listing_id).first()
        if not listing:
            #2
            raise Exception('Invalid Listing!')

        Listing.objects.create(
            game=game,
            start=start,
            end=end
        )
    #4 - Creates a mutation class with a field to be resolved,
    # which points to our mutation defined before.
        return CreateListing(id=id ,game=game,start=start,end=end)

class Mutation(graphene.ObjectType):
    create_listing = CreateListing.Field()