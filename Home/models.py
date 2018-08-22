from django.db import models

# Create your models here.
class Users(models.Model):
	user_name = models.CharField(max_length=200)
	user_email = models.EmailField(max_length=254)
	user_phone = models.IntegerField()
	user_pass = models.CharField(max_length=200)

	def __str__(self):
		return self.user_name;