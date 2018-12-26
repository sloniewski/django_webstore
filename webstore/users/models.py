from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class UserQueryset(models.QuerySet):

	def staff(self):
		return self.filter(is_staff=True)


class CustomUserManager(UserManager):
	""" some """
	def get_queryset(self):
		return UserQueryset(self.model, using=self.db)

	def staff(self):
		return self.get_queryset().staff()


class CustomUser(AbstractUser):
	objects = CustomUserManager()

	@property
	def full_name(self):
		if self.first_name and self.last_name:
			return '{} {}'.format(self.first_name, self.last_name)
		return 'not provided'
    
