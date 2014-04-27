from django.conf.urls import patterns
from fileupload.views import upload_file

urlpatterns = patterns(
    '',
    (r'^new/$', upload_file, {}, 'upload-new'),
    #(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), {}, 'upload-delete'),
)

