from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def root_route(request):
    return Response({
        'message': 'Welcome to my event drf API!'
    })
