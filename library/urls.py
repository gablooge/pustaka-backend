from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from library.views import BorrowBookView
from library.viewsets import BookViewSet

app_name = "library_app"


class OptionalSlashRouter(routers.DefaultRouter):
    def init(self):
        super()
        self.trailing_slash = "/?"


router = OptionalSlashRouter()
router.register(r"books", BookViewSet, basename="Book")

urlpatterns = [
    path("", include(router.urls)),
    url(r"^student/(?P<pk>[0-9]+)/borrow/$", BorrowBookView.as_view()),
]
