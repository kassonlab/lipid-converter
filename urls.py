from django.conf.urls import patterns,include,url
from django.views.generic import RedirectView

urlpatterns = patterns('',
                       (r'^$',RedirectView.as_view(url='/convert/main/')),
                       (r'^convert/',include('convert.urls')),
                       )

