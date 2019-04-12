from django.shortcuts import render
from .models import Sponsor, Image, Team , Event, NewsFeed, FAQ , Highlight, Achievement
from .serializers import SponsorSerializer, EventSerializer, NewsFeedSerializer, ImageSerializer, FAQSerializer ,HighlightSerializer, TeamSerializer, AchievementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.paginator import Paginator


class SponsorGetView (APIView):
    def get(self,request):
            sponsors= Sponsor.objects.all()
            serializer= SponsorSerializer(sponsors, many= True)
            return Response(serializer.data)

class SponsorPostView (APIView):
    def post(self, request): 
        serializer= SponsorSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SponsorDelView (APIView): 
    def delete(self, request,pk):
        try:
            sponsors = Sponsor.objects.get(id=pk)
        except sponsors.DoesNotExist:
            raise Http404
        sponsors.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)



class AllHighlights (APIView):
    #Function to view all highlights using URL : /api/highlight/all/
    def get(self, request):
        try:
            Highlights = Highlight.objects.all()
            serializer = HighlightSerializer(Highlights, many = True)
            return Response(serializer.data)
        except Exception:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Highlights (APIView):
    #Function to add a new highlight using URL : /api/highlight/
    def post(self, request):
        image = {}
        image["image"]=request.data["image"]
        image = ImageSerializer(data = image)
        if image.is_valid():
            image.save()
        else:
            return Response("image error")
        serializer = HighlightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["image"]= [Image.objects.last().id]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #Function to edit an already existing highlight using URL : /api/highlight/
    def put(self,request):
        image = {}
        id = request.GET.get('id', '')
        Highlights = Highlight.objects.filter(id = id).first()
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
            request.data["image"]= [Highlights.image.first().id]
        serializer= HighlightSerializer(Highlights, data= request.data)
        if serializer.is_valid():
            serializer.validated_data["image"]= request.data["image"]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #Function to delete a highlight using URL : /api/highlight/
    def delete (self, request):
        try:
            id = request.GET.get('id', '')
            Highlight.objects.filter(id = id).delete()
            return Response("Deleted successfully", status=status.HTTP_200_OK)
        except:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActiveHighlights (APIView):
    #Function to get active Highlights using url : /api/highlight/active/
    def get(self, request):
        try:
            Highlights = Highlight.objects.filter(active = "True")
            serializer = HighlightSerializer(Highlights, many = True)
            return Response(serializer.data)
        except Exception:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllEvents (APIView):
    #Function to view all events using URL : /api/events/all/
    def get(self, request):
        try:
            Events = Event.objects.all()
            serializer = EventSerializer(Events, many = True)
            return Response(serializer.data)
        except Exception:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Events (APIView):
    #Function to add a new event using URL : /api/events/
    def post(self, request):
        #to be able to send images , we must first check if image is valid , then save that image , and we will then obtain it from the
        #image table
        image = {}
        image["image"]=request.data["image"]
        image = ImageSerializer(data = image)
        if image.is_valid():
            image.save()
        else:
            return Response("image error")
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["image"]= [Image.objects.last().id]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #Function to edit an already existing event using URL : /api/events/
    def put(self,request):
        image = {}
        id = request.GET.get('id', '')
        Events = Event.objects.filter(id = id).first()
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
            request.data["image"]= [Events.image.first().id]
        serializer= EventSerializer(Events, data= request.data)
        if serializer.is_valid():
            serializer.validated_data["image"]= request.data["image"]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Function to delete an event using URL : /api/events/
    def delete(self, request):
        try:
            id = request.GET.get('id', '')
            Event.objects.filter(id = id).delete()
            return Response("Deleted successfully", status=status.HTTP_200_OK)
        except:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActiveEvents (APIView):
    #Function to get active events using url : /api/events/active/

    def get(self, request):
        try:
            Events = Event.objects.filter(status = "True")
            serializer = EventSerializer(Events, many = True)
            return Response(serializer.data)
        except Exception:
            return Response("Error ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Ach (APIView):
    def get (self, request):
        achs=Achievement.objects.all()
        serializer= AchievementSerializer(achs, many=True)
        return Response(serializer.data)

class TeamView (APIView):
    def get (self,request):
        teams= Team.objects.all()
        serializer= TeamSerializer(teams, many= True)
        return Response(serializer.data)

    def post (self, request):
        #achievement = {}  #name of the obj (JSON)-----DICTIONARY
        achievement=request.data["achievement"]  #field inside the dic , put data inside it key=value
        achievement = AchievementSerializer(data = achievement)
        if achievement.is_valid():
           achievement.save()
        else:
           return Response("achievement error ")
        image = {}
        image["image"]=request.data["image"]
        image = ImageSerializer(data = image)
        if image.is_valid():
            image.save()
        else:
            return Response("image error")
        serializer= TeamSerializer(data= request.data)
        if serializer.is_valid():
            serializer.validated_data["achievement"]=[Achievement.objects.last().id]
            serializer.validated_data["image"]= [Image.objects.last().id]
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamEditView (APIView):
    def put (self, request, pk):
        
        teams = Team.objects.filter(id = pk).first()
        achievement= request.data["achievement"]
        if(achievement != ""):
            achievement=AchievementSerializer(data= achievement)
            if achievement.is_valid():
                achievement.save()
                request.data["achievement"]=[Achievement.objects.last().id]
                print(request.data["achievement"])
            else:
                return Response("achievement")
        else:
            request.data["achievement"]=[teams.achievement.first().id]

        image = {}
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
            request.data["image"]= [teams.image.first().id]

        serializer= TeamSerializer(teams, data= request.data)
        if serializer.is_valid():
            serializer.validated_data["image"]= request.data["image"]
            serializer.validated_data["achievement"]= request.data["achievement"]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete (self, request, pk):
        try:
            teams = Team.objects.get(id=pk)
            print("teams.achievement")
            print(teams.achievement)
            for i in teams.achievement:
                Achievement.objects.filter(id=i).delete()
        except teams.DoesNotExist:
            raise Http404
        teams.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

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
    