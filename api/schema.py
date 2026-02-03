import graphene


class Query(graphene.ObjectType):
    name = graphene.String()


schema = graphene.Schema(query=Query)
