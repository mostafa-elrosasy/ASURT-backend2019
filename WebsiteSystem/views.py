from django.shortcuts import render
from .models import Sponsor, Image, Team , Event, NewsFeed, FAQ
from .serializers import SponsorSerializer, EventSerializer, NewsFeedSerializer, ImageSerializer, FAQSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.paginator import Paginator


class SponsorGetView (APIView):
    def get(self,request):
        try:
            sponsors= Sponsor.objects.all()
            serializer= SponsorSerializer(sponsors, many= True)
            return Response(serializer.data)
        except Exception :
            return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SponsorPostView (APIView):
    def post(self, request): #still has to link image table
        try:
            serializer= SponsorSerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=True)
        except Exception :
            return Response("An error has happened!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SponsorDelView (APIView): #error in url
    def delete(self, request,pk):
        try:
            sponsors = Sponsor.objects.get(id=pk)
            #serializer= SponsorSerializer(sponsors)
            #return Response(serializer.data)
        except Sponsor.DoesNotExist:
            raise Http404
        sponsors.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class Events (APIView):
    def get(self, request):
        try:
            Events = Event.objects.all()
            serializer = EventSerializer(Events, many = True)
            return Response(serializer.data)
        except Exception:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = Event.objects.create

    #Put Method to edit existing event

    #Delete Method to delete event

class ActiveEvents (APIView):
    def get(self, request):
        try:
            Events = Event.objects.filter(status = "True")
            serializer = EventSerializer(Events, many = True)
            return Response(serializer.data)
        except Exception:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TeamView (APIView):
    def get (self,request):
        pass

    def post (self, request):
        pass

class TeamEditView (APIView):
    def put (self, request, pk):
        pass
    
    def delete (self, request, pk):
        pass

class NewsFeedView(APIView):
    def get(self, request, page_number):
        data={}
        news = NewsFeed.objects.all()
        pages = Paginator(news, 2)
        page = pages.page(page_number)
        serializer = NewsFeedSerializer(page, many= True)
        data["num_pages"]=pages.num_pages
        data["articles"]= serializer.data
        return Response(data)

class EditNewsFeedView(APIView):
    def put(self,request, id):
        image = {}
        news = NewsFeed.objects.filter(id = id).first()
        image["image"]=request.data["image"]
        if(image["image"]!=""):
            image = ImageSerializer(data = image)
            if image.is_valid():
                image.save()
                request.data["image"]= [Image.objects.last().id]
                print(request.data["image"])
            else:
                return Response("image error")
        else:
            request.data["image"]= [news.image.first().id]
        serializer= NewsFeedSerializer(news, data= request.data)
        if serializer.is_valid():
            serializer.validated_data["image"]= request.data["image"]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, id):
        try:
            news = NewsFeed.objects.filter(id = id).delete()
            return Response("Deleted successfully", status=status.HTTP_200_OK)
        except:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class PostNewsFeedView(APIView):   
    def post(self, request):
        image = {}
        image["image"]=request.data["image"]
        image = ImageSerializer(data = image)
        if image.is_valid():
            image.save()
        else:
            return Response("image error")
        serializer= NewsFeedSerializer(data= request.data)
        if serializer.is_valid():
            serializer.validated_data["image"]= [Image.objects.last().id]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FAQView(APIView):
    def get(self,request):
        Faqs=FAQ.objects.all()
        serializer = FAQSerializer(Faqs, many= True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def post(self,request):
        serializer = FAQSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    