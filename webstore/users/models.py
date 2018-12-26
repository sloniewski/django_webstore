from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class UserQueryset(models.QuerySet):

	def staff(self):
		return self.filter(models.Q(is_staff=True) | models.Q(is_superuser=True))

	def clients(self):
		return self.filter(models.Q(is_staff=False) & models.Q(is_superuser=False))


class CustomUserManager(UserManager):

	def get_queryset(self):
		return UserQueryset(self.model, using=self.db)

	def staff(self):
		return self.get_queryset().staff()

	def clients(self):
		return self.get_queryset().clients()


class CustomUser(AbstractUser):
	objects = CustomUserManager()

	@property
	def full_name(self):
		if self.first_name and self.last_name:
			return '{} {}'.format(self.first_name, self.last_name)
		return 'not provided'
    
