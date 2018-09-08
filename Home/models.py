from django.db import models
from django.utils import timezone
from django.contrib import admin
import re

# Create your models here.
class Users(models.Model):
	user_name = models.CharField(max_length=200)
	user_email = models.EmailField(max_length=254)
	user_phone = models.CharField(max_length=15)
	user_pass = models.CharField(max_length=200)


	def check_validation(self):
		if len(self.user_name.strip()) == 0 or len(self.user_email.strip()) == 0 or  9 >len(self.user_phone) or len(self.user_phone)>13 or len(self.user_pass.strip()) ==0  :
			return False
		return True;

	def __str__(self):
		return self.user_name;

class Posts(models.Model):
	author = models.ForeignKey(Users, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save();

	def short(self):
		cleanText = self.cleanhtml(self.text);
		return cleanText[:300];

	def cleanhtml(self,raw_html):
		cleanr = re.compile('<.*?>');
		cleantext = re.sub(cleanr, '', raw_html);
		return cleantext;

	def check_validation(self):
		title = self.title.strip();
		text = self.text.strip();
		if( len(title) > 0 and len(text) > 10):
			return True;
		return False;

	def count_like(self):
		x = Votes.objects.filter(post_id=self,vote=True)
		return len(x)

	def __str__(self):
		return self.title;

class Votes(models.Model):
	vote = models.BooleanField(default=False)
	post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
	user_id = models.ForeignKey(Users,on_delete=models.CASCADE)

	def toggle_vote(self):
		self.vote = not self.vote;

admin.site.register(Users)
admin.site.register(Posts)
