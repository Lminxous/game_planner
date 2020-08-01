import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from game_planner.users.schema import UserType
from django.core.exceptions import ObjectDoesNotExist
from graphql_jwt.decorators import login_required
from main import models
from main.utils import find_num_hours_in_overlap, find_overlap_range 



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
   
class CreateListing(graphene.Mutation):
    listing = graphene.Field(Listing)

    class Arguments:
        game = graphene.String()
        start = graphene.DateTime()
        end = graphene.DateTime()        

    def mutate(self, info,game,start,end):
        user = info.context.user or None
        listing = models.Listing(organiser=user,game=game,start=start,end=end)
        listing.save()

        if models.Group.objects.groups_by_game(game=game):
            listing_range = (listing.start, listing.end)
            groups = models.Group.objects.groups_by_game(game=game)
            def overlap_func(g):
                return find_num_hours_in_overlap((g.start, g.end), listing_range)
            # overlap_func = lambda g: find_num_hours_in_overlap((g.start, g.end), listing_range)
            print(groups)
            print(overlap_func)
            # print(find_num_hours_in_overlap((listing_range,listing_range))
            potential_groups = []
            for group in groups:
                potential_groups.append((overlap_func(group),group))
                print(potential_groups)
            # potential_groups = list(filter(overlap_func, potential_groups))
            # print(potential_groups)
            potential_groups.sort(key=lambda x:x[0])
            potential_groups.reverse() 
            print(potential_groups)
            
            for group in groups:
                if group.members.count()<4:
                    group.members.add(listing)
                    group.save()
                    listing.group = group
                    listing.save()
                else:
                    continue

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
          
# class CreateListing(graphene.Mutation):
#     listing = graphene.Field(Listing)

#     class Arguments:
#         game = graphene.String()
#         start = graphene.DateTime()
#         end = graphene.DateTime()        

    # def mutate(self, info,game,start,end):
#         user = info.context.user or None
#         listing = models.Listing(organiser=user,game=game,start=start,end=end)
#         listing.save()

#         if models.Group.objects.groups_by_game(game=game):
#             listing_range = (listing.start, listing.end)
#             potential_groups = models.Group.objects.filter(game=game)
#             overlap_func = lambda g: find_num_hours_in_overlap((g.start, g.end), listing_range)
#             print(potential_groups)
#             print(overlap_func)
#             # print(find_num_hours_in_overlap((listing_range,listing_range))
#             # groups = filter(overlap_func, potential_groups)
#             # print(potential_groups)
#             # list(potential_groups).sort(key=overlap_func)
#             # list(potential_groups).reverse() 
#             # print(potential_groups)
            
#             for group in potential_groups:
#                 if group.members.count()<4:
#                     group.members.add(listing)
#                     group.save()
#                     listing.group = group
#                     listing.save()
#                 else:
#                     continue

#         else:
#             group = models.Group(game=game,start=start,end=end)
#             group.save()
#             group.members.add(listing)
#             group.save()
#             listing.group = group
#             listing.save()

#         return CreateListing(listing=listing)