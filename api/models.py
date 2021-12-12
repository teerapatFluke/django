from django.db import models
import datetime
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


from django.contrib.auth.hashers import make_password

# Create your models here.


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, user_name, name, password,**other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault("is_active", True)


        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True.")

        return self.create_user(user_name, name, password,**other_fields)

    def create_user(self, user_name, name, password, **other_fields):

        if not user_name:
            raise ValueError("You must provide an user_name")

        user = self.model(user_name=user_name,**other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, blank=True)
    user_picture = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=datetime.date.today)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    expo_noti = models.CharField(max_length=150, blank=True)

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
    date_add = models.DateField(default=datetime.date.today)
    chat_url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.artist_name_TH


class ArtistFollow(models.Model):
    newuser = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    

    class Meta:
        unique_together = ["newuser", "artist"]


class Request(models.Model):
    newuser = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    request_header = models.CharField(max_length=50)
    request_type = models.IntegerField(default=1)
    request_detail = models.TextField()
    request_date = models.DateField(default=datetime.date.today)
    request_read=models.IntegerField(default=0)

    def __str__(self):
        return self.request_header


class Problem(models.Model):
    newuser = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    problem_head = models.CharField(max_length=50, default="no_head")
    problem_detail = models.TextField(default="no_detail")
    problem_date = models.DateField(default=datetime.date.today)
    problem_read=models.IntegerField(default=0)

    def __str__(self):
        return self.problem_head


class Venue(models.Model):
    name = models.CharField(max_length=50)
    mapname = models.CharField(max_length=150,blank = True)
    mapurl = models.CharField(max_length=150,blank = True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=50)
    type = models.IntegerField(default=1)
    detail = models.CharField(max_length=150,blank = True)

    def __str__(self):
        return self.name


class Promoter(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    artistpost = models.ManyToManyField(Artist, blank=True)
    ticketpost = models.ManyToManyField(Ticket, blank=True)
    date = models.DateField(default=datetime.date.today)
    date_lastupdate = models.DateField(default=datetime.date.today)
    show_day = models.DateField(blank=True, null=True)
    end_day = models.DateField(blank=True, null=True)
    ticket_open = models.DateField(blank=True, null=True)
    ticket_price = models.CharField(max_length=50, blank=True)
    ticket_price_end = models.CharField(max_length=50, blank=True,null=True)
    promoter = models.ForeignKey(
        Promoter, on_delete=models.CASCADE, blank=True, null=True
    )
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, blank=True, null=True)
    detail_update = models.CharField(
        max_length=50, default="เพิ่มข้อมูลเข้าสู่ระบบ")
    event_follower = models.IntegerField(default=0)
    complete = models.IntegerField(default=0)

    def __str__(self):
        return self.event_name


class EventFollow(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'event',)

class AmazonKey(models.Model):
    accessKey = models.CharField(max_length=100)
    secretKey = models.CharField(max_length=100)

class Noification(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today, blank=True, null=True)
    class Meta:
        unique_together = ["event", "date"]
    def __str__(self):
        return "%s (%s)" % (
            self.tile,
            ", ".join(event.id for event in self.event.all()),
        )


class ChatRoom(models.Model):
    artist =models.ForeignKey(Artist, on_delete=models.CASCADE)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('artist', 'user',)
