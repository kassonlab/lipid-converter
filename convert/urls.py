from django.conf.urls import patterns,include,url

urlpatterns = patterns('',
                       url(r'^main/$','convert.views.main'),
                       url(r'^convert/$','convert.views.convert'),
                       url(r'^transform/$','convert.views.transform'),
                       url(r'^help/$','convert.views.help'),
                       url(r'^references/$','convert.views.references'),
                       url(r'^results/$','convert.views.results'),
                       url(r'^download/(?P<file_id>(.*)/$)','convert.views.download'),
                       )

