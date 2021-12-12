from django.shortcuts import render
import django_filters
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
import stream_chat
from .models import (
    Artist,
    ArtistFollow,
    NewUser,
    Request,
    Problem,
    Venue,
    Ticket,
    Promoter,
    Event,
    EventFollow,
    AmazonKey,Noification,ChatRoom
)
from .serializers import (
    ArtistSerializer,
    ArtistFollowSerializer,
    NewuserSerializer,
    NotificationSerializer,
    RequestSerializer,
    ProblemSerializer,
    VenueSerializer,
    TicketSerializer,
    EventSerializer,
    EventFollowSerializer,
    PromoterSerializer,
    AmazonSerializer,NotificationSerializer,ChatRoomSerializer
)
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action


class ArtistFollowFilter(django_filters.FilterSet):
    newuser = django_filters.NumberFilter(field_name="newuser")
    artist = django_filters.NumberFilter(field_name="artist")

    class Meta:
        model = ArtistFollow
        fields = []


class EventFollowFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name="user")
    event = django_filters.NumberFilter(field_name="event")



    class Meta:
        model = EventFollow
        fields = []


class NotificationFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="date")
    event = django_filters.NumberFilter(field_name="event")

    class Meta:
        model = Noification
        fields = []

class EventFilter(django_filters.FilterSet):
    complete = django_filters.NumberFilter(field_name="complete")
    artist = django_filters.NumberFilter(field_name="artistpost")
    event_name = django_filters.CharFilter(field_name='event_name', method='my_custom_filter')

    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("show_day", "show_day"),
            ("ticket_open", "ticket_open"),
            ("date", "date"),
        ),
    )
    a = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ("show_day", "show_day"),
            ("ticket_open", "ticket_open"),
        ),
    )

    def my_custom_filter(self, queryset, name, value):
        event_name = value
        return queryset.filter(event_name__icontains=event_name )



    class Meta:
        model = Event
        fields = []

class ChatRoomFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name="user")
    artist = django_filters.NumberFilter(field_name="artist")

    class Meta:
        model = ChatRoom
        fields = []

class RequestFilter(django_filters.FilterSet):
    request_read = django_filters.NumberFilter(field_name="request_read")

    class Meta:
        model = Request
        fields = []

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = NewuserSerializer

    def post(self, request):
        reg_serializer = NewuserSerializer(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                return Response(
                    reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=True, methods=['post'])
    def expo_token(self, request, pk=None):
        re = request.data
        user = NewUser.objects.get(id=pk)
        user.expo_noti = re["expo_noti"]
        user.save()
        response = {user.expo_noti}
        return Response(response, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['post'])
    def update_user(self,request, pk=None):
        data = request.data
        u = NewUser.objects.get(id=pk)
        if(str(data["user_name"]) !=""):
            if(data["user_name"] != data["old_user"]):
                k = NewUser.objects.filter(user_name=data["user_name"]).exists() 
                if(k):
                    return Response(k, status=status.HTTP_200_OK)
                else:
                    u.user_name = data["user_name"]
            
                 
        if(str(data["picture"]) !=""):
            u.user_picture = data["picture"]
        if(str(data["password"]) !=""):
            u.set_password(data["password"])          
        u.save()
        response = {data["password"]}
        return Response(response, status=status.HTTP_200_OK)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["user_id"] = user.id
        token["is_staff"] = user.is_staff
        token["name"]=user.name
        token["user_name"]=user.user_name
        token["user_picture"] = user.user_picture

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all().order_by('artist_name_EN')
    serializer_class = ArtistSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['artist_name_EN', 'artist_name_TH']


    @action(detail=True, methods=['post'])
    def addfollwer(self, request, pk=None):
        artist = Artist.objects.get(id=pk)
        artist.artist_follow =artist.artist_follow+1
        artist.save()
        response = {artist.artist_follow}
        return Response(response, status=status.HTTP_200_OK)

    
    @action(detail=True, methods=['post'])
    def unfollower(self, request, pk=None):
        artist = Artist.objects.get(id=pk)
        artist.artist_follow =artist.artist_follow-1
        artist.save()
        response = {artist.artist_follow}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_chaturl(self, request, pk=None):
        artist = Artist.objects.get(id=pk)
        re = request.data
        artist.chat_url = re["url"]
        artist.save()
        response = {artist.chat_url}
        return Response(response, status=status.HTTP_200_OK)






class ArtistFollowViewSet(viewsets.ModelViewSet):
    queryset = ArtistFollow.objects.all()
    serializer_class = ArtistFollowSerializer
    filterset_class = ArtistFollowFilter


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all().order_by('request_read')
    serializer_class = RequestSerializer
    filterset_class = RequestFilter

    @action(detail=True, methods=['post'])
    def requestread(self, request, pk=None):
        request = Request.objects.get(id=pk)
        request.request_read = 1
        request.save()
        response = {request.request_read}
        return Response(response, status=status.HTTP_200_OK)


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all().order_by('problem_read')
    serializer_class = ProblemSerializer

    @action(detail=True, methods=['post'])
    def problemread(self, request, pk=None):
        problem = Problem.objects.get(id=pk)
        problem.problem_read = 1
        problem.save()
        response = {problem.problem_read}
        return Response(response, status=status.HTTP_200_OK)


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        return Response(request.data)


class PromoterViewSet(viewsets.ModelViewSet):
    queryset = Promoter.objects.all()
    serializer_class = PromoterSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter


    @action(detail=True, methods=['post'])
    def addfollwer(self, request, pk=None):
        event = Event.objects.get(id=pk)
        event.event_follower =event.event_follower+1
        event.save()
        response = {event.event_follower}
        return Response(response, status=status.HTTP_200_OK)

    
    @action(detail=True, methods=['post'])
    def unfollower(self, request, pk=None):
        event = Event.objects.get(id=pk)
        event.event_follower =event.event_follower-1
        event.save()
        response = {event.event_follower}
        return Response(response, status=status.HTTP_200_OK)


class EventFollowViewSet(viewsets.ModelViewSet):
    queryset = EventFollow.objects.select_related('event').all()
    serializer_class = EventFollowSerializer
    filterset_class = EventFollowFilter


class AmazonViewSet(viewsets.ModelViewSet):
    queryset = AmazonKey.objects.all()
    serializer_class = AmazonSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Noification.objects.all()
    serializer_class = NotificationSerializer
    filterset_class = NotificationFilter

   
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    filterset_class = ChatRoomFilter



   
