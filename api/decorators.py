from functools import wraps
from graphql import GraphQLError


def login_required_graphql(f):
    @wraps(f)
    def wrapper(self, info, *args, **kwargs):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication required")
        return f(self, info, *args, **kwargs)

    return wrapper
