from django.db import models


class ProductManager(models.Manager):

    def all_active(self):
        return self.filter(deleted_at=None)
