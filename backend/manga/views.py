from django.shortcuts import render
from rest_framework import viewsets
from .models import Series
from .serializers import SeriesSerializer


# Create your views here.
class SeriesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing manga series.
    """
    # This tells the view what data to get from the database
    queryset = Series.objects.all()

    # This tells the view what serializer to use for translating the data
    serializer_class = SeriesSerializer