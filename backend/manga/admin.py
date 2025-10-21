from django.contrib import admin
from .models import Series

# Register your models here.
@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    # This shows these columns in the admin list view
    list_display = ('title', 'mangadex_id', 'status')
    
    # This adds a search bar
    search_fields = ('title', 'mangadex_id')