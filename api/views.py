from django.shortcuts import render
import django_filters
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
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
    AmazonKey,Noification
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
    AmazonSerializer,NotificationSerializer
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


class EventFilter(django_filters.FilterSet):
    complete = django_filters.NumberFilter(field_name="complete")
    artist = django_filters.NumberFilter(field_name="artistpost")

    class Meta:
        model = Event
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
    def streamtoken(self, request, pk=None):
        server_client = stream_chat.StreamChat(api_key="j93zaqtvjdfu", api_secret="3j65a48kk65g9jwj9xywqbrgd33ng9reyd5us2xs73r4kymbvch7jbyr33bcmvqw") 
        token = server_client.create_token(str(pk))
        response = {token}
        return Response(response, status=status.HTTP_200_OK)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["user_id"] = user.id
        token["is_staff"] = user.is_staff
        token["name"]=user.name
        token["user_picture"] = user.user_picture

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ArtistFollowViewSet(viewsets.ModelViewSet):
    queryset = ArtistFollow.objects.all()
    serializer_class = ArtistFollowSerializer
    filterset_class = ArtistFollowFilter


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


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

   
