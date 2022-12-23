from django.urls import include, path
from rest_framework import routers

from library.viewsets import BookViewSet

app_name = "library_app"


class OptionalSlashRouter(routers.DefaultRouter):
    def init(self):
        super().init()
        self.trailing_slash = "/?"


router = OptionalSlashRouter()
router.register(r"books", BookViewSet, basename="Book")

urlpatterns = [path("", include(router.urls))]
