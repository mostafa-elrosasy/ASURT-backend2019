from rest_framework import serializers
from RT_Website_19.fields import Base64FileField
from .models import Sponsor, Event, NewsFeed, Image, FAQ

class ImageSerializer(serializers.ModelSerializer):
    image = Base64FileField(max_length=None)

    class Meta:
        model = Image
        fields = '__all__'

class SponsorSerializer (serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)
    class Meta:
        model = Sponsor
        fields = '__all__'

class EventSerializer (serializers.ModelSerializer):
    image = ImageSerializer(read_only=True, many=True)
    class Meta:
        model = Event
        fields = '__all__'

        
class NewsFeedSerializer (serializers.ModelSerializer):
    image = ImageSerializer(read_only=True, many=True)
    class Meta:
        model = NewsFeed
        fields = '__all__'

class FAQSerializer (serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = '__all__'


