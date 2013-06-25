from sorl.thumbnail import get_thumbnail
from ss.programming.models import Season, Film, Gig, Event, Festival, Programmer, Rating, Meeting, FILM_FORMATS, MEETING_TYPES
from ss.content.models import Page, Menu, Document, DOC_TYPE
from ss.content.forms import PageForm, DocumentForm
from ss.fileupload.models import Picture
from ss.organisation.models import Minutes, PrintProgramme, Approval, ApprovalSet
from ss.organisation.forms import SeasonAdminForm, FilmAdminForm, GigAdminForm, EventAdminForm, FestivalAdminForm, MeetingAdminForm, MinutesForm
from django.contrib import messages
from django.utils import simplejson
from django.http import HttpResponse
from django.db.models import get_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import datetime
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import Resource, ModelResource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization


class SelectSeasonResource(ModelResource):
    class Meta:
        queryset = Season.objects.all().order_by('title')
        fields = ['title', 'id']
        allowed_methods = ['get', ]


class SelectProgrammerResource(ModelResource):
    class Meta:
        queryset = Programmer.objects.all().order_by('name')
        fields = ['name', 'id']
        allowed_methods = ['get', ]


class SelectMeetingResource(ModelResource):
    class Meta:
        queryset = Meeting.objects.all().order_by('start')
        fields = ['title', 'id']
        allowed_methods = ['get', ]


class SelectRatingResource(ModelResource):
    class Meta:
        queryset = Rating.objects.all().order_by('name')
        fields = ['name', 'id']
        allowed_methods = ['get', ]


class SelectCertificateResource(ModelResource):
    class Meta:
        resource_name = 'certificate'
        queryset = Rating.objects.all().order_by('name')
        fields = ['name', 'id']
        allowed_methods = ['get', ]


class SelectPictureResource(ModelResource):
    src = fields.CharField(attribute='src', default="")
    height = fields.CharField(attribute='height', default="100")
    width = fields.CharField(attribute='width', default="100")
    thumbnailSrc = fields.CharField(attribute='thumbnailSrc', default="")
    thumbnailHeight = fields.CharField(attribute='thumbnailHeight', default="100")
    thumbnailWidth = fields.CharField(attribute='thumbnailWidth', default="100")
    displaySrc = fields.CharField(attribute='displaySrc', default="")
    displayHeight = fields.CharField(attribute='displayHeight', default="400")
    displayWidth = fields.CharField(attribute='displayWidth', default="400")
    class Meta:
        queryset = Picture.objects.all().order_by('-modified', '-id')
        allowed_methods = ['get', ]


class PlainFilmFormat(object):
    def __init__(self, ff=None):
        if ff is not None:
            self.id = ff[0]
            self.name = ff[1]


class SelectFilmFormatResource(Resource):
    id = fields.CharField(attribute='id')
    name = fields.CharField(attribute='name')

    class Meta:
        object_class = PlainFilmFormat

    def obj_get_list(self, request=None, **kwargs):
        return [PlainFilmFormat(ff) for ff in FILM_FORMATS]


class SelectApprovalResource(ModelResource):
    class Meta:
        queryset = Approval.objects.all()
        # TODO fields = ['title', 'id']
        allowed_methods = ['get', ]


class SelectMenuResource(ModelResource):
    class Meta:
        queryset = Menu.objects.all()
        # TODO fields = ['title', 'id']
        allowed_methods = ['get', ]


class PageResource(ModelResource):
    menu = fields.ForeignKey(SelectMenuResource, 'menu')

    class Meta:
        queryset = Page.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()


class SeasonResource(ModelResource):
    picture = fields.ForeignKey(SelectPictureResource, 'picture', null=True)
    programmer = fields.ForeignKey(SelectProgrammerResource, 'programmer')
    approval = fields.ForeignKey(SelectApprovalResource, 'approval')

    class Meta:
        queryset = Season.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()


class FilmResource(ModelResource):
    certificate = fields.ForeignKey(SelectRatingResource, 'certificate')
    season = fields.ForeignKey(SelectSeasonResource, 'season')
    picture = fields.ForeignKey(SelectPictureResource, 'picture', null=True)
    programmer = fields.ForeignKey(SelectProgrammerResource, 'programmer')
    approval = fields.ForeignKey(SelectApprovalResource, 'approval')

    class Meta:
        queryset = Film.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()


class GigResource(ModelResource):
    picture = fields.ForeignKey(SelectPictureResource, 'picture', null=True)
    programmer = fields.ForeignKey(SelectProgrammerResource, 'programmer')
    approval = fields.ForeignKey(SelectApprovalResource, 'approval')

    class Meta:
        queryset = Gig.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()


class EventResource(ModelResource):
    picture = fields.ForeignKey(SelectPictureResource, 'picture', null=True)
    programmer = fields.ForeignKey(SelectProgrammerResource, 'programmer')
    approval = fields.ForeignKey(SelectApprovalResource, 'approval')

    class Meta:
        queryset = Event.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()


class FestivalResource(ModelResource):
    # TODO picture = fields.ForeignKey(SelectPictureResource, 'picture')
    programmer = fields.ForeignKey(SelectProgrammerResource, 'programmer')
    approval = fields.ForeignKey(SelectApprovalResource, 'approval')
    films = fields.ManyToManyField(FilmResource, 'films')
    gigs = fields.ManyToManyField(GigResource, 'events')
    events = fields.ManyToManyField(EventResource, 'events')

    class Meta:
        queryset = Festival.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()


class MeetingResource(ModelResource):
    programmer = fields.ForeignKey(SelectProgrammerResource, 'programmer')
    approval = fields.ForeignKey(SelectApprovalResource, 'approval')

    class Meta:
        queryset = Meeting.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()


class MinutesResource(ModelResource):
    meeting = fields.ForeignKey(MeetingResource, 'meeting')

    class Meta:
        queryset = Minutes.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()


class DocumentResource(ModelResource):
    class Meta:
        queryset = Document.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()


class MinutesResource(ModelResource):
    class Meta:
        queryset = Picture.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()

        #-----------------------------------


        # class SeasonSelectHandler(BaseHandler):
        #     allowed_methods = ('GET',)
        #
        #     def read(self, request, *args, **kwargs):
        #         return [{'label': item.title, 'id': item.id, 'url': item.get_absolute_url()} for item in Season.objects.all().order_by('title')]
        #
        #
        # class ProgrammerSelectHandler(BaseHandler):
        #     allowed_methods = ('GET',)
        #
        #     def read(self, request, *args, **kwargs):
        #         return [{'label': item.name, 'id': item.id, 'url': item.get_absolute_url()} for item in Programmer.objects.all().order_by('name')]
        #
        #
        # class MeetingSelectHandler(BaseHandler):
        #     allowed_methods = ('GET',)
        #
        #     def read(self, request, *args, **kwargs):
        #         return [{'label': item.longHeading, 'id': item.id, 'url': item.get_absolute_url()} for item in Meeting.objects.all().order_by('start')]
        #
        #
        # class RatingSelectHandler(BaseHandler):
        #     allowed_methods = ('GET',)
        #
        #     def read(self, request, *args, **kwargs):
        #         return [{'label': item.name, 'id': item.id, 'url': '/'} for item in Rating.objects.all().order_by('name')]
        #
        #
        # class FilmformatSelectHandler(BaseHandler):
        #     allowed_methods = ('GET',)
        #
        #     def read(self, request, *args, **kwargs):
        #         return [{'label': filmFormat[0], 'id': filmFormat[0], 'url': '/'} for filmFormat in FILM_FORMATS]
        #
        #
        # class DocumenttypeSelectHandler(BaseHandler):
        #     allowed_methods = ('GET',)
        #
        #     def read(self, request, *args, **kwargs):
        #         return [{'label': dt[0], 'id': dt[0], 'url': '/'} for dt in DOC_TYPE]
        #
        #
        # class MeetingtypeSelectHandler(BaseHandler):
        #     allowed_methods = ('GET',)
        #
        #     def read(self, request, *args, **kwargs):
        #         return [{'label': meetingtype[0], 'id': meetingtype[0], 'url': '/'} for meetingtype in MEETING_TYPES]
        #
        #
        # class GraphicSelectHandler(BaseHandler):
        #     allowed_methods = ('GET',)
        #
        #     def read(self, request, *args, **kwargs):
        #         start = int(request.GET.get('page', '0')) * 35
        #         pictures = Picture.objects.order_by('-modified', '-id')[start:start + 35]
        #         result = []
        #         for pic in pictures:
        #             try:
        #                 thumb = get_thumbnail(pic.file, '100x100', crop='top')
        #                 image = get_thumbnail(pic.file, '400')
        #                 result.append({
        #                     'id': pic.id,
        #                     'label': pic.slug,
        #                     'url': pic.file.name,
        #                     'thumb': {
        #                         'src': thumb.url,
        #                         'height': thumb.height,
        #                         'width': thumb.width
        #                     },
        #                     'image': {
        #                         'src': image.url,
        #                         'height': image.height,
        #                         'width': image.width
        #                     }
        #                 })
        #             except IOError:
        #                 result.append({
        #                     'id': 1,
        #                     'label': 'error',
        #                     'url': 'error',
        #                     'thumb': {
        #                         'src': 'error',
        #                         'height': 100,
        #                         'width': 100,
        #                     },
        #                     'image': {
        #                         'src': 'error',
        #                         'height': 100,
        #                         'width': 100
        #                     }
        #                 })
        #         return result
        #
        #
        # class PageSelectHandler(BaseHandler):
        #     allowed_methods = ('GET',)
        #
        #     def read(self, request, *args, **kwargs):
        #         return [{'label': item.linkText, 'id': item.id, 'url': item.relativeUrl()} for item in Page.objects.all().order_by('linkText')]
        #
        #
        # class MenuSelectHandler(BaseHandler):
        #     allowed_methods = ('GET',)
        #
        #     def read(self, request, *args, **kwargs):
        #         return [{'label': item.linkText, 'id': item.id, 'url': item.linkText} for item in Menu.objects.all().order_by('linkText')]
        #
        #
        # @csrf_exempt
        # def getPrintProgrammeData(request):
        #     printProgrammeData = {'sections': []}
        #     try:
        #         year = int(request.REQUEST.get('year', None))
        #         month = int(request.REQUEST.get('month', None))
        #         if year is None or month is None or year not in range(2000, 2040) or month not in range(1, 13):
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid date for print programme data'}), mimetype="application/json")
        #     except ValueError:
        #         return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid date for print programme data'}), mimetype="application/json")
        #     fordate = datetime(year=int(year), month=int(month), day=1)
        #     try:
        #         programme = PrintProgramme.objects.filter(start__lte=fordate, end__gt=fordate)
        #         programme = programme[0]
        #         startMonth = programme.start.strftime('%B')
        #         endMonth = programme.end.strftime('%B')
        #         startYear = programme.start.strftime('%Y')
        #         endYear = programme.end.strftime('%Y')
        #         if startMonth == endMonth:
        #             printProgrammeData['title'] = '%s %s' % (startMonth, startYear)
        #         else:
        #             if startYear == endYear:
        #                 printProgrammeData['title'] = '%s - %s %s' % (startMonth, endMonth, startYear)
        #             else:
        #                 printProgrammeData['title'] = '%s %s - %s %s' % (startMonth, startYear, endMonth, endYear)
        #         printProgrammeData['sections'].append(programme.embedcode)
        #         return HttpResponse(simplejson.dumps(printProgrammeData), mimetype="application/json")
        #     except IndexError:
        #         return HttpResponse(simplejson.dumps({'title': 'Not Found', 'sections': ['<p>This brochure has not been uploaded yet.  Sorry.</p>', ]}), mimetype="application/json")
        #
        #
        # # noinspection PyBroadException
        # @login_required
        # def approvalsSetMeeting(request):
        #     approvalsMeeting = request.REQUEST.get('approvals-meeting', None)
        #     if approvalsMeeting is None:
        #         request.session['approvals-currently'] = False
        #         request.session['approvals-meeting'] = None
        #         return HttpResponse(simplejson.dumps({'status': 'success', 'message': 'Approving stopped.'}), mimetype="application/json")
        #     else:
        #         try:
        #             meeting = Meeting.objects.get(id=int(approvalsMeeting))
        #             request.session['approvals-currently'] = True
        #             request.session['approvals-meeting'] = meeting.id
        #             return HttpResponse(simplejson.dumps({
        #                 'status': 'success',
        #                 'approvals-meeting': meeting.id,
        #                 'message': 'Approving items for meeting %s <a href="#" class="button stopapproving">Finish Approving</a>' % meeting.id,
        #             }), mimetype="application/json")
        #         except:
        #             request.session['approvals-currently'] = False
        #             request.session['approvals-meeting'] = None
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'error'}), mimetype="application/json")
        #
        #
        # # noinspection PyBroadException
        # @login_required
        # def approveProgrammeItem(request):
        #     if request.user.is_authenticated():  # TODO: This is where we need to think about who is allowed to approve events.  There should be a more sophisticated test here.
        #         itemtype = request.REQUEST.get('itemtype', None)
        #         itemid = request.REQUEST.get('itemid', None)
        #         meetingid = request.REQUEST.get('meetingid', None)
        #
        #         # Syntactically valid data
        #         if itemid is None or meetingid is None or itemtype not in ['Season', 'Film', 'Gig', 'Event', 'Festival', 'Meeting']:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid data for approval'}), mimetype="application/json")
        #         try:
        #             itemid = int(itemid)
        #             meetingid = int(meetingid)
        #             model = get_model('programming', itemtype)
        #         except:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid data for approval'}), mimetype="application/json")
        #
        #         # Legitimate values
        #         try:
        #             meeting = Meeting.objects.get(id=meetingid)
        #         except ObjectDoesNotExist:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid meeting id %s for approval' % meetingid}), mimetype="application/json")
        #         try:
        #             programmer = Programmer.objects.get(user=request.user)
        #         except ObjectDoesNotExist:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid user %s for approval' % request.user}), mimetype="application/json")
        #         try:
        #             item = model.objects.get(id=itemid)
        #         except ObjectDoesNotExist:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid event %s %s for approval' % (itemtype, itemid)}), mimetype="application/json")
        #         if item.approval is not None:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Item %s %s already approved' % (itemtype, itemid)}), mimetype="application/json")
        #
        #         # Get the approvalset for the meeting, or create one if it doesn't already exist
        #         try:
        #             approvalSet = ApprovalSet.objects.get(meeting=meeting)
        #         except ObjectDoesNotExist:
        #             approvalSet = ApprovalSet(meeting=meeting)
        #             approvalSet.save()
        #
        #         try:
        #             approval = Approval(approvalset=approvalSet, approver=programmer)
        #             approval.save()
        #         except:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'error, failed saving approval'}), mimetype="application/json")
        #         try:
        #             item.approval = approval
        #             item.save()
        #             item.approval.save()
        #             message = 'Successfully approved "%s"' % item.title
        #             messages.success(request, message)
        #             return HttpResponse(simplejson.dumps({'status': 'success', 'message': message}), mimetype="application/json")
        #         except:
        #             # Avoid having a dangling approval if its connection to the item failed.
        #             approval.delete()
        #     return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'error, failed unknown'}), mimetype="application/json")
        #
        #
        # # noinspection PyBroadException
        # @login_required
        # def unapproveProgrammeItem(request):
        #     if request.user.is_authenticated():  # TODO: This is where we need to think about who is allowed to approve events.  There should be a more sophisticated test here.
        #         itemtype = request.REQUEST.get('itemtype', None)
        #         itemid = request.REQUEST.get('itemid', None)
        #
        #         # Syntactically valid data
        #         if itemid is None or itemtype not in ['Season', 'Film', 'Gig', 'Event', 'Festival', 'Meeting']:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid data for removing approval'}), mimetype="application/json")
        #         try:
        #             itemid = int(itemid)
        #             model = get_model('programming', itemtype)
        #         except:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid data for removing approval'}), mimetype="application/json")
        #
        #         # Legitimate values
        #         try:
        #             item = model.objects.get(id=itemid)
        #         except ObjectDoesNotExist:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid event %s %s for removing approval' % (itemtype, itemid)}), mimetype="application/json")
        #         if item.approval is None:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Item %s %s not approved' % (itemtype, itemid)}), mimetype="application/json")
        #
        #         #try:
        #         item.approval.delete()
        #         item.approval = None
        #         item.save()
        #         message = 'Successfully removed approval "%s"' % item.title
        #         messages.success(request, message)
        #         return HttpResponse(simplejson.dumps({'status': 'success', 'message': message}), mimetype="application/json")
        #         #except:
        #         #    pass  # TODO: What if the approval deletes but the item save fails?
        #     return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'error'}), mimetype="application/json")
        #
        #
        # # noinspection PyBroadException
        # @login_required
        # def confirmItem(request):
        #     if request.user.is_authenticated():  # TODO: This is where we need to think about who is allowed to confirm events.  There should be a more sophisticated test here.
        #         itemtype = request.REQUEST.get('itemtype', None)
        #         itemid = request.REQUEST.get('itemid', None)
        #         confirm = request.REQUEST.get('confirm', None)
        #
        #         # Syntactically valid data
        #         if itemid is None or itemtype not in ['Season', 'Film', 'Gig', 'Event', 'Festival', 'Meeting']:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid data for toggling confirmation'}), mimetype="application/json")
        #         try:
        #             confirm = simplejson.loads(confirm)
        #             itemid = int(itemid)
        #             model = get_model('programming', itemtype)
        #         except:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid data for toggling confirmation'}), mimetype="application/json")
        #
        #         # Legitimate values
        #         try:
        #             item = model.objects.get(id=itemid)
        #         except ObjectDoesNotExist:
        #             return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'Invalid event %s %s for toggling confirmation' % (itemtype, itemid)}), mimetype="application/json")
        #
        #         #try:
        #         item.confirmed = confirm
        #         item.save()
        #         if confirm:
        #             message = 'Successfully confirmed "%s"' % item.title
        #         else:
        #             message = 'Successfully unconfirmed "%s"' % item.title
        #         messages.success(request, message)
        #         return HttpResponse(simplejson.dumps({'status': 'success', 'message': message}), mimetype="application/json")
        #     return HttpResponse(simplejson.dumps({'status': 'error', 'message': 'error'}), mimetype="application/json")
        #
        #
        # def getItemFromRequest(request):
        #     itemtype = request.REQUEST.get('itemtype', None)
        #     itemid = request.REQUEST.get('itemid', None)
        #     if itemid is None or itemtype not in ['Season', 'Film', 'Gig', 'Event', 'Festival', 'Meeting']:
        #         raise ValidationError
        #     try:
        #         itemid = int(itemid)
        #         model = get_model('programming', itemtype)
        #     except:
        #         raise ValidationError
        #     return model.objects.get(id=itemid)
        #
        #
        # # noinspection PyUnusedLocal
        # @login_required
        # def getApprovalData(request):
        #     approvalData = {'sections': []}
        #     #event = getItemFromRequest(request)
        #
        #     # User authorisation
        #     approvalData['sections'].append(
        #         '<div class="message warning"><img class="imgright" src="/static/icon_alert.gif" height="16" width="16" alt=""/>This system does not currently restrict who can approve events.  Please do not approve events unless authorised to do so by a Monday meeting.</div>')
        #     #if request.user.is_authenticated():  # TODO: This is where we need to think about who is allowed to approve events.  There should be a more sophisticated test here.
        #     #    approvalData['sections'].append('<div class="message info"><img class="imgright" src="/static/icon_success.gif" height="16" width="16" alt=""/>You are authorised to approve events.</div>')
        #     #else:
        #     #    approvalData['sections'].append('<div class="message error"><img class="imgright" src="/static/icon_error.gif" height="16" width="16" alt=""/>You are not authorised to approve events.</div>')
        #
        #     # Organiser detail
        #     approvalData['sections'].append(
        #         '<div class="message warning"><img class="imgright" src="/static/icon_alert.gif" height="16" width="16" alt=""/>This system does not check the contact details for event organisers.  Please check that the listed programmer has entered their contact details before approving the event.</div>')
        #     #if event.programmer.valid:  # TODO: Assess validity of programmer
        #     #    approvalData['sections'].append('<div class="message info"><img class="imgright" src="/static/icon_success.gif" height="16" width="16" alt=""/>The event organiser, %s, has supplied valid contact details.</div>' % event.programmer.get_link)
        #     #else:
        #     #    approvalData['sections'].append('<div class="message error"><img class="imgright" src="/static/icon_error.gif" height="16" width="16" alt=""/>The event organiser, %s, has not supplied valid contact details:<ul><li>%s</li></ul></div>' % (event.programmer.get_link, '</li><li>'.join(event.programmer.validityMessages)))
        #
        #     # Event Details
        #     approvalData['sections'].append(
        #         '<div class="message warning"><img class="imgright" src="/static/icon_alert.gif" height="16" width="16" alt=""/>This system does not yet check the validity of event details.  Before approving this event please make sure that the details have been filled in correctly.</div>')
        #     #if event.valid:  # TODO: proper testing of validity
        #     #    approvalData['sections'].append('<div class="message info"><img class="imgright" src="/static/icon_success.gif" height="16" width="16" alt=""/>The details for this event are valid.</div>')
        #     #else:
        #     #    approvalData['sections'].append('<div class="message error"><img class="imgright" src="/static/icon_error.gif" height="16" width="16" alt=""/>The details for this event not valid:<ul><li>%s</li></ul></div>' % '</li><li>'.join(event.validityMessages))
        #
        #     # Clashes
        #     # TODO: This needs a whole load of extra thinking
        #     #approvalData['sections'].append('<div class="message info"><img class="imgright" src="/static/icon_success.gif" height="16" width="16" alt=""/>This event does not appear to conflict with any other events.<div class="message warning"><img class="imgright" src="/static/icon_alert.gif" height="16" width="16" alt=""/>This automated test is imperfect and should not be relied on.  Please check manually to make sure there are no conflicts.</div></div>')
        #     approvalData['sections'].append(
        #         '<div class="message warning"><img class="imgright" src="/static/icon_alert.gif" height="16" width="16" alt=""/>This system does not yet check for double bookings.  Please check manually to make sure this event does not conflict with any other events.</div>')
        #
        #     # Finance Plan
        #     approvalData['sections'].append(
        #         '<div class="message warning"><img class="imgright" src="/static/icon_alert.gif" height="16" width="16" alt=""/>This system does not check the finance plans for events.  A valid finance plan may not have been submitted.</div>')
        #     #if event.financeform is not None: # TODO: Finance form logic
        #     #    if event.financeform.valid:
        #     #        approvalData['sections'].append('<div class="message info"><img class="imgright" src="/static/icon_success.gif" height="16" width="16" alt=""/>The <a>finance form</a> for this event has been submitted and is valid.</div>')# % event.financeform.get_link)
        #     #    else:
        #     #        approvalData['sections'].append('<div class="message error"><img class="imgright" src="/static/icon_error.gif" height="16" width="16" alt=""/>The <a>finance form</a> for this event is not valid:<ul><li>%s</li></ul></div>')# % (event.financeform.get_link, '</li><li>'.join(event.financeform.validityMessages)))
        #     #else:
        #     #    approvalData['sections'].append('<div class="message error">No finance form has been submitted for this event</div>')
        #
        #     # License requirements
        #     # TODO: Three-way test: Finishes during, finishes after normal hours and has a late license request, finishes after normal hours and doesn't have a late license request.
        #     approvalData['sections'].append(
        #         '<div class="message warning"><img class="imgright" src="/static/icon_alert.gif" height="16" width="16" alt=""/>This system does not yet check license requirements for events.  If this event takes place outside of the normal licensing hours then a late license application may be required.</div>')
        #
        #     # Create list of meetings and select the nearest in time.
        #     meetingSelect = ''
        #     nowdate = datetime.today()
        #     meetings = Meeting.objects.filter(startDate__lte=nowdate).order_by('-startDate')
        #     meetingId = meetings[0].id
        #     for meeting in meetings:
        #         if meeting.id == meetingId:
        #             meetingSelect += '<option value="%s" selected>%s</option>' % (meeting.id, meeting.longHeading)
        #         else:
        #             meetingSelect += '<option value="%s">%s</option>' % (meeting.id, meeting.longHeading)
        #     approvalData['sections'].append('<div class="message">Select the meeting that approved this event:</p><p><ul><li><select id="meetingselectlist">' + meetingSelect + '</select></li></ul></div>')
        #     approvalData['sections'].append('<p class="center"><a class="button approveitem" href="#">Approve</a></p>')
        #
        #     return HttpResponse(simplejson.dumps(approvalData), mimetype="application/json")