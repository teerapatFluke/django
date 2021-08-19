from django.shortcuts import render
from .models import Artist, ArtistFollow, NewUser, Request, Problem, Venue, Ticket, Promoter, Event, EventFollow, \
    ArtistEvent, TicketEvent
from .serializers import ArtistSerializer, ArtistFollowSerializer, NewuserSerializer, RequestSerializer, \
    ProblemSerializer, VenueSerializer, TicketSerializer, EventSerializer, EventFollowSerializer, \
    ArtistEventSerializer, TicketEventSerializer, PromoterSerializer
from rest_framework import viewsets


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = NewuserSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ArtistFollowViewSet(viewsets.ModelViewSet):
    queryset = ArtistFollow.objects.all()
    serializer_class = ArtistFollowSerializer


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


class PromoterViewSet(viewsets.ModelViewSet):
    queryset = Promoter.objects.all()
    serializer_class = PromoterSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventFollowViewSet(viewsets.ModelViewSet):
    queryset = EventFollow.objects.all()
    serializer_class = EventFollowSerializer


class ArtistEventViewSet(viewsets.ModelViewSet):
    queryset = ArtistEvent.objects.all()
    serializer_class = ArtistEventSerializer


class TicketEventViewSet(viewsets.ModelViewSet):
    queryset = TicketEvent.objects.all()
    serializer_class = TicketEventSerializer
