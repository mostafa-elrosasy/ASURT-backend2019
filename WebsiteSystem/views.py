from django.shortcuts import render
from .models import Sponsor
from .serializers import SponsorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SponsorView (APIView):
    def get(self,request):
        try:
            sponsors= Sponsor.objects.all()
            serializer= SponsorSerializer(sponsors, many= True)
            return Response(serializer.data)
        except Exception :
            return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer= SponsorSerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=True)
        except Exception :
            return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request):
        try:
            sponsers = Sponsor.objects.filter().first
            sponsers.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response ("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


