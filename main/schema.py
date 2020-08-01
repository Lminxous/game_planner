import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from game_planner.users.schema import UserType
from django.core.exceptions import ObjectDoesNotExist
from graphql_jwt.decorators import login_required
from main import models
from main.utils import find_num_mins_in_overlap, find_overlap_range 


# Types
class Listing(DjangoObjectType):
    class Meta:
        model = models.Listing
        fields = ['id', 'player','game', 'group','start', 'end',] 

class Group(DjangoObjectType):
    class Meta:
        model = models.Group
        fields = ['id','game',]

class Query(graphene.ObjectType):
    all_groups = graphene.List(Group)
    group_by_id = graphene.Field(Group, id=graphene.Int())
    group_by_game = graphene.List(Group, game=graphene.String())
    all_listings = graphene.List(Listing)

    @login_required
    def resolve_all_groups(self, info, **kwargs):
        return models.Group.objects.all()

    @login_required
    def resolve_group_by_id(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            try:
                return models.Group.objects.get(id=id)
            except ObjectDoesNotExist:
                return None    
        return None

    @login_required
    def resolve_group_by_game(self, info, **kwargs):
        game = kwargs.get('game')

        if game is not None:
            try:
                return models.Group.objects.filter(game=game)
            except ObjectDoesNotExist:
                return None    
        return None    

    @login_required
    def resolve_all_listings(self, info,**kwargs):
        return models.Listing.objects.all()
   
class CreateListing(graphene.Mutation):
    listing = graphene.Field(Listing)

    class Arguments:
        game = graphene.String()
        start = graphene.DateTime()
        end = graphene.DateTime()        

    def mutate(self, info,game,start,end):
        user = info.context.user or None
        listing = models.Listing(player=user,game=game,start=start,end=end)
        listing.save()

        # Fetching half-filled groups with specified game            
        half_filled_groups = models.Group.objects.filter(game=game,is_full=False)

        if half_filled_groups:
            listing_range = (listing.start, listing.end)
            # Groups with specified game arranged in order of max overlap
            def overlap_func(g):
                return find_num_mins_in_overlap((g.start, g.end), listing_range)
            potential_groups = []
            for group in half_filled_groups:
                potential_groups.append((overlap_func(group),group))
                # print(potential_groups)       
            potential_groups.sort(key=lambda x:x[0])
            potential_groups.reverse()     
            print(potential_groups)       

            overlap_ranges = []
            for group in potential_groups:
                # Adding listing in half filled group with max overlap   
                group_range = (group[1].start, group[1].end)
                overlap_range = find_overlap_range(group_range, listing_range) 
                if overlap_range == None:
                    pass
                else: 
                    group_range = (group[1].start, group[1].end)
                    overlap_range = find_overlap_range(group_range, listing_range) 
                    group[1].start = overlap_range[0]
                    group[1].end = overlap_range[1]
                    group[1].members.add(listing)
                    group[1].save()
                    listing.group = group[1]
                    listing.save()
                    break   
            
            # If there is no overlap with the previous half filled groups of specified game
            if potential_groups[0][0] == 0:
                    group = models.Group(game=game,start=start,end=end)
                    group.save()
                    group.members.add(listing)
                    group.save()
                    listing.group = group
                    listing.save()
                           
        
        # If there are no previous groups of the specified game
        else:
            group = models.Group(game=game,start=start,end=end)
            group.save()
            group.members.add(listing)
            group.save()
            listing.group = group
            listing.save()

        return CreateListing(listing=listing)
          
    
class Mutation(graphene.ObjectType):
    create_listing = CreateListing.Field()
          
