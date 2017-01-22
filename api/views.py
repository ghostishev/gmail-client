from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from social_django.utils import psa
from gmail_api import get_message_by_id, get_message_list
from rest_framework import status

# Define an URL entry to point to this view, call it passing the
# access_token parameter like ?access_token=<token>. The URL entry must
# contain the backend, like this:
#
#   url(r'^register-by-token/(?P<backend>[^/]+)/$',
#       'register_by_access_token')
from api.models import MessageModel
from api.serializers import MessageSerializer


@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    access_token = request.GET.get('access_token')
    user = request.backend.do_auth(access_token,
                                   response={'access_token': access_token})
    if user:
        login(request, user)
        return 'OK'
    else:
        return 'ERROR'


class MessageView(APIView):
    """
    View to get one message from DB
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, message_id):
        """
        Return a list of all users.
        """
        access_token = request.META.get('HTTP_TOKEN')
        if not access_token:
            return Response({'error': 'Wrong access token'}, status=status.HTTP_401_UNAUTHORIZED)

        source = 'internal DB'
        try:
            message = MessageModel.objects.get(message_id=message_id)
            snippet = message.snippet
        except MessageModel.DoesNotExist:
            snippet_from_google = get_message_by_id(access_token, message_id)
            snippet = snippet_from_google
            if snippet_from_google:
                message_model = MessageModel(message_id=message_id, snippet=snippet_from_google)
                message_model.save()
                source = 'GMail API'

        return Response({'data': snippet, 'source': source})


class MessageListView(APIView):
    """
    View recent 100 emails from GMail
    """

    def get(self, request):
        access_token = request.META.get('HTTP_TOKEN')
        if not access_token:
            return Response({'error': 'Wrong access token'}, status=status.HTTP_401_UNAUTHORIZED)
        recent_100_messages = get_message_list(access_token)
        recent_100_snippets = []
        for message_id in recent_100_messages:
            try:
                message = MessageModel.objects.get(message_id=message_id)
                recent_100_snippets.append(message.snippet)
            except MessageModel.DoesNotExist:
                snippet_from_google = get_message_by_id(access_token, message_id)
                recent_100_snippets.append(snippet_from_google)
                if snippet_from_google:
                    message_model = MessageModel(message_id=message_id, snippet=snippet_from_google)
                    message_model.save()
        return Response(recent_100_snippets)
