from django.conf.urls import patterns
from fileupload.views import upload_file, image_info

urlpatterns = patterns(
    '',
    (r'^new/$', upload_file, {}, 'upload-new'),
    (r'^info/(?P<pk>\d+)$', image_info, {}, 'image-info'),
    #(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), {}, 'upload-delete'),
)

