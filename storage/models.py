from django.db import models


class Part(models.Model):
    """
    Model for the parts that was used by the tickets
    """
    part = models.CharField(max_length=30)

    def __str__(self):
        return self.part

