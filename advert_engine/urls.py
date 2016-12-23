from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('advert_engine.api.urls')),
    # url(r'^admin', AdminView.as_view(), name='admin'),
    # url(r'^', HomeView.as_view(), name='home'),
]
