import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphql_jwt.decorators import login_required
from main import models
from main.schema.types import (Listing,Group)

class Query:
    all_groups = graphene.List(Group)
    group = graphene.Field(Group, game=graphene.String())
    listing = graphene.Field(Listing, id=graphene.Int())
    all_listings = graphene.Field(Listing)


    @login_required
    def resolve_all_groups(self, info, **kwargs):
        return models.Group.objects.all()

    @login_required
    def resolve_group(self, info, **kwargs):
        game = kwargs.get('game')

        if game is not None:
            return models.Group.objects.get(game=game)
        return None

    @login_required
    def resolve_listing(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            try:
                return models.Listing.objects.get(id=id)
            except ObjectDoesNotExist:
                return None
        return None

    @login_required
    def resolve_all_listings(self, info,**kwargs):
        return models.Listing.objects.all()

    
