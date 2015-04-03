from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from dateutil.relativedelta import *
from django.core.urlresolvers import reverse

from programming.models import Picture
import content.forms
from lib.utils import Prog


def page(request, linkText=''):
    if linkText == '':
        page = get_object_or_404(content.forms.Page, linkText='home')
    else:
        page = get_object_or_404(content.forms.Page, linkText=linkText)
    if page.linkText == 'home':
        prog = Prog(startDate=date.today(), endDate=(date.today() + relativedelta(weeks=2)), approved=True).byDate(
            trimmed=True)
    else:
        prog = None
    return render_to_response('page.html',
                              {
                                  'maintitle': page.title,
                                  'event': page,
                                  'fillerImage': Picture.objects.get(id=789),
                                  'prog': prog,
                              },
                              context_instance=RequestContext(request)
    )


def pageSignup(request):
    page = get_object_or_404(content.forms.Page, linkText='signup')
    return render_to_response('signup.html',
                              {
                                  'maintitle': page.title,
                                  'event': page,
                                  'fillerImage': Picture.objects.get(id=789),
                                  'prog': None,
                              },
                              context_instance=RequestContext(request)
    )

@login_required
def documentEdit(request, id=None):
    if id is None:
        item = content.forms.Document()
    else:
        item = get_object_or_404(content.forms.Document, id=id)
    if request.method == 'POST':
        form = content.forms.DocumentForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(item.get_absolute_url())
    else:
        form = content.forms.DocumentForm(instance=item)
    return render_to_response('content/documentEdit.html',
                              {
                                  'maintitle': 'Edit / Add Document',
                                  'item': item,
                                  'form': form,
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def documentAdd(request):
    doc = content.forms.Document()
    doc.title = "New document"
    doc.author = "AUTHOR"
    doc.created = timezone.now().date()
    doc.body = "New document"
    doc.save()
    return redirect(reverse('view-document', kwargs={'documentId': doc.pk}))


def documentView(request, documentId=None):
    doc = get_object_or_404(content.forms.Document, id=documentId)
    return render_to_response('content/document.html',
                              {
                                  'maintitle': doc.title,
                                  'event': doc,
                              },
                              context_instance=RequestContext(request)
    )


def documentList(request):
    docs = content.forms.Document.objects.all().order_by('-created')
    return render_to_response('content/documentList.html',
                              {
                                  'maintitle': 'Reviews',
                                  'docs': docs,
                              },
                              context_instance=RequestContext(request)
    )
