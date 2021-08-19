from rest_framework import serializers
from .models import Artist, NewUser, ArtistFollow, Request, Problem, Venue, Ticket, Promoter, Event, EventFollow, \
    ArtistEvent, TicketEvent


class NewuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = [
            "user_name",
            "name",
            "user_picture",
            "is_staff"
        ]


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [
            "id",
            "artist_name_TH",
            "artist_name_EN",
            "artist_picture",
            "artist_follow",
            "date_add"
        ]


class ArtistFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistFollow
        fields = ["id", "newuser", "artist", "date"]
        depth = 0


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ["id", "newuser", "request_header", "request_type", "request_detail", "request_date"]
        depth = 0


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ["id", "newuser", "problem_head", "problem_detail", "problem_date"]


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "name"]


class PromoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promoter
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "event_name", "date", "date_lastupdate", "show_day", "end_day", "ticket_open", "ticket_price",
                  "promoter", "promoter", "venue", "detail_update", "event_follower"]
        depth = 1


class EventFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFollow
        fields = ["id", "user", "event"]


class ArtistEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistEvent
        fields = ["id", "artist", "event"]


class TicketEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketEvent
        fields = ["id", "ticket", "event"]