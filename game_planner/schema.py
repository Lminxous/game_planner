import graphene
import graphql_jwt
import main.schema
from .users import schema

class Query(schema.Query,main.schema.Query, graphene.ObjectType):
    pass

class Mutation(schema.Mutation, main.schema.Mutation, graphene.ObjectType,):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)