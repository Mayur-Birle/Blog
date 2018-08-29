from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.
class Users(models.Model):
	user_name = models.CharField(max_length=200)
	user_email = models.EmailField(max_length=254)
	user_phone = models.CharField(max_length=15)
	user_pass = models.CharField(max_length=200)

	def __str__(self):
		return self.user_name;

class Posts(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def short(self):
    	return self.text[:300];

    def __str__(self):
        return self.title;

admin.site.register(Users)
admin.site.register(Posts)
