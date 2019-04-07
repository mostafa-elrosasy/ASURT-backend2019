from rest_framework import serializers
from RT_Website_19.fields import Base64FileField
from .models import Sponsor

class SponsorSerializer (serializers.ModelSerializer):
    image = Base64FileField(max_length=None)
    class Meta:
        model = Sponsor
        fields = '__all__'
