from django.urls import path

from .apps import NetworkConfig
from .views import (
    NetworkEntityCreateView,
    NetworkEntityDetailView,
    NetworkEntityUpdateView,
    NetworkEntityDeleteView,
    NetworkEntityListView
)


app_name = NetworkConfig.name

urlpatterns = [
    path('network/', NetworkEntityListView.as_view(), name='networkentity-list'),
    path('network/create/', NetworkEntityCreateView.as_view(), name='networkentity-create'),
    path('network/<int:pk>/', NetworkEntityDetailView.as_view(), name='networkentity-detail'),
    path('network/<int:pk>/update/', NetworkEntityUpdateView.as_view(), name='networkentity-update'),
    path('network/<int:pk>/delete/', NetworkEntityDeleteView.as_view(), name='networkentity-delete'),
]
