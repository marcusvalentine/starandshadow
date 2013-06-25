from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from ss.content.models import *
from ss.content.forms import *
from ss.lib.utils import Prog
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from dateutil.relativedelta import *
from datetime import date

def page(request, linkText=''):
    if linkText == '':
        page = get_object_or_404(Page, linkText='home')
    else:
        page = get_object_or_404(Page, linkText=linkText)
    if page.linkText == 'home':
        prog = Prog(startDate=date.today(), endDate=(date.today() + relativedelta(weeks=2)), approved=True).byDate(trimmed=True)
    else:
        prog = None
    return render_to_response('page.html',
                              {
                               'maintitle': page.title,
                               'page': page,
                               'prog': prog,
                               },
                              context_instance=RequestContext(request)
                              )

@login_required
def documentEdit(request, id=None):
    if id is None:
        item = Document()
    else:
        item = get_object_or_404(Document, id=id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(item.get_absolute_url())
    else:
        form = DocumentForm(instance=item)
    return render_to_response('content/documentEdit.html',
                              {
                               'maintitle': 'Edit / Add Document',
                               'item': item,
                               'form': form,
                              },
                              context_instance=RequestContext(request)
                              )

def documentView(request, id=None):
    if id == '0' and request.user.is_authenticated():
        doc = Document()
        doc.title = "New document"
        doc.author = "AUTHOR"
        doc.created = timezone.now().date()
        doc.body = "New document"
    else:
        doc = get_object_or_404(Document, id=id)
    return render_to_response('content/document.html',
                              {
                               'maintitle': doc.title,
                               'doc': doc,
                              },
                              context_instance=RequestContext(request)
                              )

def documentList(request):
    docs = Document.objects.all().order_by('-created')
    return render_to_response('content/documentList.html',
                              {
                               'maintitle': 'Reviews',
                               'docs': docs,
                              },
                              context_instance=RequestContext(request)
                              )
