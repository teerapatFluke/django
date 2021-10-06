from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import (
    Artist,
    NewUser,
    ArtistFollow,
    Request,
    Problem,
    Venue,
    Ticket,
    Promoter,
    Event,
    EventFollow,
    AmazonKey,
    Noification
)


class NewuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ["user_name", "name", "user_picture",
                  "is_staff", "password", "expo_noti"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [
            "id",
            "artist_name_TH",
            "artist_name_EN",
            "artist_picture",
            "artist_follow",
            "date_add","chat_url"
        ]


class ArtistFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistFollow
        fields = ["id", "newuser", "artist", "date"]
        depth = 0


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = [
            "id",
            "newuser",
            "request_header",
            "request_type",
            "request_detail",
            "request_date",
        ]
        depth = 0


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ["id", "newuser", "problem_head",
                  "problem_detail", "problem_date"]


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name","mapname","mapurl"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "name","type","detail"]


class PromoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promoter
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "event_name",
            "artistpost",
            "ticketpost",
            "date",
            "date_lastupdate",
            "show_day",
            "end_day",
            "ticket_open",
            "ticket_price",
            "promoter",
            "venue",
            "detail_update",
            "event_follower",
            "complete",
        ]
        depth = 0


class EventFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFollow
        fields = ["id", "user", "event"]


class AmazonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmazonKey
        fields = ["accessKey", "secretKey"]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noification
        fields = ["id","title", "body", "event","date"]
        depth = 0


