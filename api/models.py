from django.db import models
import datetime
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, user_name, name, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(user_name, name, password, **other_fields)

    def create_user(self, user_name, name, password, **other_fields):

        if not user_name:
            raise ValueError("You must provide an user_name")

        user = self.model(user_name=user_name, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, blank=True)
    user_picture = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=datetime.datetime.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.user_name


class Artist(models.Model):
    artist_name_TH = models.CharField(max_length=50)
    artist_name_EN = models.CharField(max_length=50)
    artist_picture = models.CharField(max_length=200, blank=True)
    artist_follow = models.IntegerField(default=0)
    date_add = models.DateField(default=datetime.datetime.now)

    def __str__(self):
        return self.artist_name_TH


class ArtistFollow(models.Model):
    newuser = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.now)

    class Meta:
        unique_together = [['newuser', 'artist']]


class Request(models.Model):
    newuser = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    request_header = models.CharField(max_length=50)
    request_type = models.IntegerField(default=1)
    request_detail = models.TextField()
    request_date = models.DateField(default=datetime.datetime.now)

    def __str__(self):
        return self.request_header


class Problem(models.Model):
    newuser = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    problem_head = models.CharField(max_length=50, default="no_head")
    problem_detail = models.TextField(default="no_detail")
    problem_date = models.DateField(default=datetime.datetime.now)

    def __str__(self):
        return self.problem_head


class Venue(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Promoter(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    date = models.DateField(default=datetime.datetime.now)
    date_lastupdate = models.DateField(default=datetime.datetime.now)
    show_day = models.DateField()
    end_day = models.DateField()
    ticket_open = models.DateField()
    ticket_price = models.CharField(max_length=50)
    promoter = models.ForeignKey(Promoter, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    detail_update = models.CharField(max_length=50)
    event_follower = models.IntegerField(default=0)

    def __str__(self):
        return self.event_name


class ArtistEvent(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class TicketEvent(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class EventFollow(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
