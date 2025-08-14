from django.urls import path
from .views import DeleteURL, ShortenURL, RedirectURL, URLListView

urlpatterns = [
    path('api/shorten/', ShortenURL.as_view(), name='shorten_url'),
    path('<str:short_code>/', RedirectURL.as_view(), name='redirect_url'),
    path('api/list/', URLListView.as_view(), name='url_list'),
    path('api/delete/<int:pk>/', DeleteURL.as_view(), name='delete_url'),
]
