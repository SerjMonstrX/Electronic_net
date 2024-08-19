from django.urls import path
from .views import (
    NetworkEntityCreateView,
    NetworkEntityDetailView,
    NetworkEntityUpdateView,
    NetworkEntityDeleteView,
    NetworkEntityListView
)

urlpatterns = [
    path('network-entities/', NetworkEntityListView.as_view(), name='networkentity-list'),
    path('network-entities/create/', NetworkEntityCreateView.as_view(), name='networkentity-create'),
    path('network-entities/<int:pk>/', NetworkEntityDetailView.as_view(), name='networkentity-detail'),
    path('network-entities/<int:pk>/update/', NetworkEntityUpdateView.as_view(), name='networkentity-update'),
    path('network-entities/<int:pk>/delete/', NetworkEntityDeleteView.as_view(), name='networkentity-delete'),
]