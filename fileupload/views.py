from fileupload.models import Picture
from django.http import HttpResponse, HttpResponseNotAllowed
import simplejson as json
from django.core.files import File
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404


def upload_file(request):
    if request.method == 'POST':
        try:
            filename = request.FILES.keys()[0]
            file = File(request.FILES[filename])
            picture = Picture(
                slug=request.GET.get('slug'),
            )
            picture.file.save(file.name, file)
            picture.save()
            print picture.modified
            print picture.slug
            print picture.file.name
            data = {"success": True}
        except:
            data = {
                'error': 'invalid image data',
                'errors': 'something went wrong',
            }
        return HttpResponse(json.dumps(data), mimetype="application/json")
    return HttpResponseNotAllowed(['POST', ])


def image_info(request, pk):
    i = get_object_or_404(Picture, pk=pk)
    data = {'data': {}}
    attributes = [
        'id',
        'file',
        'src',
        'width',
        'height',
        'thumbnailSrc',
        'thumbnailWidth',
        'thumbnailHeight',
        'displaySrc',
        'displayWidth',
        'displayHeight',
    ]
    for attribute in attributes:
        data['data'][attribute] = getattr(i, attribute)
    data['attributes'] = attributes
    return render_to_response('fileupload/image_info.html',
                              data,
                              context_instance=RequestContext(request)
    )