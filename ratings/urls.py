from django.urls import path, register_converter

from . import converters, views

register_converter(converters.FloatConverter, 'float')

urlpatterns = [
    path('rate/<int:ct>/<pk>/<float:score>/', views.rate_object, name='ratings_rate_object'),
    path('unrate/<int:ct>/<pk>/', views.rate_object, {'add': False}, name='ratings_unrate_object'),
]
