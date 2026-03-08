from django.urls import path
from .views import CountryDetailHTMLView, CountryToursHTMLView,TourDetailHTMLView

urlpatterns = [
    path("country/<int:pk>/", CountryDetailHTMLView.as_view(), name="country_detail_html_ui"),
    path("country/<int:pk>/tours/", CountryToursHTMLView.as_view(), name="country_tours_html_ui"),
    path("tour/<int:pk>/", TourDetailHTMLView.as_view(), name="tour_detail_html_ui"),
]