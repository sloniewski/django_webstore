from django.db import models


class CategoryManager(models.Manager):

    def form_choices(self):
        return [x.form_choice for x in self.get_queryset().all()]
