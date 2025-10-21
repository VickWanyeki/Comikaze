# manga/management/commands/fetch_manga.py
import requests
from django.core.management.base import BaseCommand
from manga.models import Series

API_URL = "https://api.mangadex.org"

class Command(BaseCommand):
    help = 'Fetches a list of manga and their covers from the MangaDex API.'

    def get_cover_url(self, manga_data):
        """Helper function to find the cover art URL."""
        manga_id = manga_data.get('id')

        # Find the cover_art relationship
        for rel in manga_data.get('relationships', []):
            if rel.get('type') == 'cover_art':
                file_name = rel.get('attributes', {}).get('fileName')
                if file_name:
                    # Construct the full cover URL
                    return f"https://uploads.mangadex.org/covers/{manga_id}/{file_name}"
        return None

    def handle(self, *args, **options):
        self.stdout.write("Starting to fetch manga from MangaDex...")

        try:
            # Fetch 10 manga, ordered by relevance, and include cover art data
            response = requests.get(
                f"{API_URL}/manga",
                params={
                    "limit": 10, 
                    "order[relevance]": "desc",
                    "includes[]": "cover_art"  # This is key!
                }
            )
            response.raise_for_status() # Raise error for bad responses
            data = response.json()

            if data.get('result') != 'ok':
                self.stdout.write(self.style.ERROR("API did not return 'ok'"))
                return

            new_series_count = 0
            for manga_data in data.get('data', []):
                attributes = manga_data.get('attributes', {})

                # Get English title
                title_obj = attributes.get('title', {})
                title = title_obj.get('en', list(title_obj.values())[0] if title_obj else 'No Title')

                # Get English description
                desc_obj = attributes.get('description', {})
                description = desc_obj.get('en', 'No description available.')

                # Get the cover URL using our helper
                cover_url = self.get_cover_url(manga_data)

                # Use update_or_create to avoid duplicates
                series, created = Series.objects.update_or_create(
                    mangadex_id=manga_data.get('id'),
                    defaults={
                        'title': title,
                        'description': description,
                        'status': attributes.get('status', 'unknown'),
                        'cover_image_url': cover_url
                    }
                )

                if created:
                    new_series_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created: {title}'))
                else:
                    self.stdout.write(f'Updated: {title}')

            self.stdout.write(self.style.SUCCESS(f"\nDone! Created {new_series_count} new series."))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"HTTP Request failed: {e}"))