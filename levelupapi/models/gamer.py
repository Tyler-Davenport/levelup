from django.db import models


class Gamer(models.Model):
    # Unique identifier for the gamer (from Firebase or other auth)
    uid = models.CharField(max_length=50)

    # Short biography or description
    bio = models.CharField(max_length=50)

    # Display name for the gamer
    display_name = models.CharField(max_length=100, null=True, blank=True)
