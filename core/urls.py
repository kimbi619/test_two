from django.urls import path
from .views import PersonListView

app_name = 'core'

urlpatterns = [
    path('', PersonListView.as_view(), name='person-list'),
]
