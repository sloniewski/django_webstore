from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    
    @property
    def full_name(self):
    	if self.first_name and self.last_name:
    		return '{} {}'.format(self.first_name, self.last_name)
    	return 'not provided'
    
