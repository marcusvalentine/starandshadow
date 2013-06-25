from fileupload.models import Picture
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import simplejson
from django.core.files import File

def upload_file(request):
    if request.method == 'POST':
        try:
            filename = request.FILES.keys()[0]
            file = File(request.FILES[filename])
            picture = Picture(
                slug = request.GET.get('slug'),
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
                'errors' : 'something went wrong',
            }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    return HttpResponseNotAllowed(['POST',])