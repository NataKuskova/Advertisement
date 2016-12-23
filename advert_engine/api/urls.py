from django.conf.urls import url, include
from rest_framework import routers
from advert_engine.api import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'adverts', views.AdvertListViewSet)
router.register(r'gallery', views.GalleryViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^adverts/(?P<pk>\d|\w|\-)/$', views.AdvertDetailView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
