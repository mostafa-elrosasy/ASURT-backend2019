from rest_framework import serializers
from RT_Website_19.fields import Base64FileField
from .models import Sponsor, Event, NewsFeed, Image

class SponsorSerializer (serializers.ModelSerializer):
    image = Base64FileField(max_length=None)
    class Meta:
        model = Sponsor
        fields = '__all__'

class EventSerializer (serializers.ModelSerializer):
    image = Base64FileField(max_length=None)
    class Meta:
        model = Event
        fields = '__all__'

class NewsFeedSerializer (serializers.ModelSerializer):
    class Meta:
        model = NewsFeed
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    image = Base64FileField(max_length=None)

    class Meta:
        model = Image
        fields = '__all__'

