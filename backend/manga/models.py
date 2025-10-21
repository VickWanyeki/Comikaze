from django.db import models

# Create your models here.
class Series(models.Model):
    title = models.CharField(max_length=255)
    mangadex_id = models.CharField(max_length=100, unique=True, help_text="The MangaDex UUID")
    description = models.TextField(blank=True, null=True)
    cover_image_url = models.URLField(blank=True, null=True, max_length=500)
    status = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Series" # Fixes "Seriess" in admin