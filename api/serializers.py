from rest_framework import serializers

from api.models import MessageModel


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MessageModel
        fields = ('snippet', )
