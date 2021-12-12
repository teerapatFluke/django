from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import (
    ArtistViewSet,
    ArtistFollowViewSet,
    UserViewSet,
    RequestViewSet,
    ProblemViewSet,
    VenueViewSet,
    TicketViewSet,
    PromoterViewSet,
    EventViewSet,
    EventFollowViewSet,
    AmazonViewSet,
    NotificationViewSet,ChatRoomViewSet,
)

router = routers.DefaultRouter()
router.register("user", UserViewSet, basename="user")
router.register("artist", ArtistViewSet)
router.register("artistfw", ArtistFollowViewSet)
router.register("request", RequestViewSet)
router.register("venue", VenueViewSet)
router.register("ticket", TicketViewSet)
router.register("promoter", PromoterViewSet)
router.register("event", EventViewSet)
router.register("eventfw", EventFollowViewSet)
router.register("problem", ProblemViewSet)
router.register("amazon", AmazonViewSet)
router.register("notification", NotificationViewSet)
router.register("chatroom", ChatRoomViewSet)

urlpatterns = [
    path("", include(router.urls)),
  
]
