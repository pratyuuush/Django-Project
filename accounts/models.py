from django.db import models
from django.core.validators import MaxValueValidator
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.utils import timezone




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('UserProfile',
                                       related_name="followed_by",
                                       blank=True)
    image = ProcessedImageField(upload_to='profile_pics',
                                      format='JPEG',
                                      options={'quality': 100},
                                      null=True,
                                      blank=True, default='default.jpg')

    bio = models.CharField(max_length=200, null=True, blank=True, default = " ")
    AC_TYPE = (
        ('Individual', 'Individual'),
        ('Organization', 'Organization'),
    )

    

    email = models.EmailField(max_length=70)
    ac_type = models.CharField(max_length=12, choices=AC_TYPE, default=" ")

    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
        blank=False,
        default=" "
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
        blank=False, 
        default=" "
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=10,
        blank=False, 
        default=" "
    )

    city = models.CharField(
        max_length=1024,
        blank=False, 
        default=" "
    )
    state = models.CharField(
        max_length=1024,
        blank=False, 
        default=" "
    )
    country = CountryField(
        blank_label='Select Country')

    phone = PhoneNumberField(blank=False,null=True)
    
    feeds = models.ManyToManyField('Post',
                            related_name="Feed",
                            blank=True)

    def follow_user(self, follower):
        return self.following.add(follower)

    def unfollow_user(self, to_unfollow):
        return self.following.remove(to_unfollow)

    def is_following(self, checkuser):
        return checkuser in self.following.all()

    def get_number_of_followers(self):
        if self.followers.count():
                return self.followers.count()
        else:
                return 0

          

    def get_number_of_following(self):
        if self.following.count():
            return self.following.count()
        else:
            return 0

    def __str__(self):
        return self.user.username

class Post(models.Model):
    post_something = models.TextField(max_length=1000, null=True, blank=False)
    posted_on = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

    POST_TYPE = (
        ('Job', 'Job'),
        ('Blg', 'Blog'),
    )
    post_type = models.CharField(max_length=3, choices=POST_TYPE)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')

    def save(self, **kwargs):
        super().save()

    
