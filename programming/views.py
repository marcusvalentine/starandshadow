from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from programming.models import Programmer, Rating, Season, Film, Gig, Event, Festival, Meeting, Picture, FilmFormat
from organisation.models import ApprovalSet
from lib.utils import ssDate, Prog
from django.utils import timezone
from datetime import date, time


def listHome(request):
    return listPeriod(request, date.today(), size='week', title='Coming Up', earliertext='Last Week',
                      latertext='Next Week')


def listToday(request):
    return listPeriod(request, date.today(), size='day', title='Today', earliertext='Yesterday', latertext='Tomorrow')


def listWeek(request):
    return listPeriod(request, date.today(), size='week', title='This Week', earliertext='Last Week',
                      latertext='Next Week')


def listNextWeek(request):
    return listPeriod(request, date.today() + timezone.timedelta(days=7), size='week', title='Next Week',
                      earliertext='This Week')


def listMonth(request):
    return listPeriod(request, date.today(), size='month', title=date.today().strftime('%B %Y'), earliertext='Earlier',
                      latertext='Later')


def listNextMonth(request):
    return listPeriod(request, date.today() + timezone.timedelta(days=30), size='month', title='Next Month',
                      earliertext='This Month')


def listPeriod(request, dateObj=None, **kwargs):
    cal = ssDate(dateObj, **kwargs)
    prog = Prog(cal=cal, public=True, approved=True)
    return render_to_response('programming/listPeriod.html',
                              {
                                  'maintitle': kwargs['title'] if 'title' in kwargs else unicode(cal),
                                  'earliertext': kwargs['earliertext'] if 'earliertext' in kwargs else 'Earlier',
                                  'latertext': kwargs['latertext'] if 'latertext' in kwargs else 'Later',
                                  'fillerImage': Picture.objects.get(id=789),
                                  'cal': cal,
                                  'prog': prog.byDate(),
                              },
                              context_instance=RequestContext(request)
    )


def season(request, id):
    if id == '0' and request.user.is_authenticated():
        event = Season()
        event.programmer = Programmer.objects.get(user=request.user)
        event.endDate = date.today()
        try:
            year = int(request.GET['year'])
            month = int(request.GET['month'])
            if year in range(1970,2050) and month in range(1,13):
                event.startDate = date(year, month, 1)
            else:
                event.startDate = date.today()
        except:
            event.startDate = date.today()
        event.save()
    else:
        event = get_object_or_404(Season, id=id)
        if not request.user.is_authenticated():
            if event.deleted or not event.confirmed:
                raise Http404
    prog = Prog(type=[Film.objects, ], season=event, public=True, approved=True)
    return render_to_response('programming/season.html',
                              {
                                  'maintitle': event.title,
                                  'event': event,
                                  'extramessage': event.extramessage(request),
                                  'prog': prog.byDate(),
                                  'fillerImage': Picture.objects.get(id=789),
                              },
                              context_instance=RequestContext(request)
    )


def film(request, id):
    if id == '0' and request.user.is_authenticated():
        event = Film()
        event.programmer = Programmer.objects.get(user=request.user)
        event.director = 'Unknown'
        event.certificate = Rating.objects.get(pk=1)
        event.season = None
        event.filmFormat = FilmFormat.objects.get(pk=1)
        event.startTime = time(19, 30)
        try:
            year = int(request.GET['year'])
            month = int(request.GET['month'])
            if year in range(1970,2050) and month in range(1,13):
                event.startDate = date(year, month, 1)
            else:
                event.startDate = date.today()
        except:
            event.startDate = date.today()
        event.save()
    else:
        event = get_object_or_404(Film, id=id)
        if not request.user.is_authenticated():
            if event.deleted or not event.confirmed:
                raise Http404
    if event.season is None:
        event.season = Season.objects.get(id=2)
        prog = None
    else:
        prog = Prog(type=[Film.objects, ], season=event.season, public=True, approved=True)
        prog = prog.byDate()
    return render_to_response('programming/film.html',
                              {
                                  'maintitle': event.title,
                                  'event': event,
                                  'extramessage': event.extramessage(request),
                                  'prog': prog,
                                  'fillerImage': Picture.objects.get(id=789),
                              },
                              context_instance=RequestContext(request)
    )


def gig(request, id):
    if id == '0' and request.user.is_authenticated():
        event = Gig()
        event.programmer = Programmer.objects.get(user=request.user)
        event.startTime = time(19, 30)
        event.endTime = time(19, 30)
        try:
            year = int(request.GET['year'])
            month = int(request.GET['month'])
            if year in range(1970,2050) and month in range(1,13):
                event.startDate = date(year, month, 1)
            else:
                event.startDate = date.today()
        except:
            event.startDate = date.today()
        event.save()
    else:
        event = get_object_or_404(Gig, id=id)
        if not request.user.is_authenticated():
            if event.deleted or not event.confirmed:
                raise Http404
    return render_to_response('programming/gig.html',
                              {
                                  'maintitle': event.title,
                                  'extramessage': event.extramessage(request),
                                  'event': event,
                                  'fillerImage': Picture.objects.get(id=789),
                              },
                              context_instance=RequestContext(request)
    )


def event(request, id):
    if id == '0' and request.user.is_authenticated():
        event = Event()
        event.programmer = Programmer.objects.get(user=request.user)
        event.startTime = time(19, 30)
        event.endTime = time(19, 30)
        try:
            year = int(request.GET['year'])
            month = int(request.GET['month'])
            if year in range(1970,2050) and month in range(1,13):
                event.startDate = date(year, month, 1)
            else:
                event.startDate = date.today()
        except:
            event.startDate = date.today()
        event.save()
    else:
        event = get_object_or_404(Event, id=id)
        if not request.user.is_authenticated():
            if event.deleted or not event.confirmed:
                raise Http404
    return render_to_response('programming/event.html',
                              {
                                  'maintitle': event.title,
                                  'event': event,
                                  'extramessage': event.extramessage(request),
                                  'fillerImage': Picture.objects.get(id=789),
                              },
                              context_instance=RequestContext(request)
    )


def festival(request, id):
    if id == '0' and request.user.is_authenticated():
        event = Festival()
        event.programmer = Programmer.objects.get(user=request.user)
        event.startDate = date.today()
        event.startTime = time(19, 30)
        event.endDate = date.today()
        event.endTime = time(19, 30)
    else:
        event = get_object_or_404(Festival, id=id)
        if not request.user.is_authenticated():
            if event.deleted or not event.confirmed:
                raise Http404
    prog = Prog(festival=event, public=True, approved=True)
    return render_to_response('programming/festival.html',
                              {
                                  'maintitle': event.title,
                                  'event': event,
                                  'extramessage': event.extramessage(request),
                                  'prog': prog.byDate(),
                                  'fillerImage': Picture.objects.get(id=789),
                              },
                              context_instance=RequestContext(request)
    )


def meeting(request, id):
    if id == '0' and request.user.is_authenticated():
        event = Meeting()
        event.programmer = Programmer.objects.get(id=183)
        event.startTime = time(19, 30)
        meetingInFuture = True
        approvalSet = None
        try:
            year = int(request.GET['year'])
            month = int(request.GET['month'])
            if year in range(1970,2050) and month in range(1,13):
                event.startDate = date(year, month, 1)
            else:
                event.startDate = date.today()
        except:
            event.startDate = date.today()
        event.save()
    else:
        event = get_object_or_404(Meeting, id=id)
        if not request.user.is_authenticated():
            if event.deleted or not event.confirmed:
                raise Http404
        if event.startDateTime > timezone.now():
            meetingInFuture = True
            # Meeting starts in the future, so cannot have approvalSet.  We're ignoring the fact that one nevertheless may exist.
            approvalSet = None
        else:
            meetingInFuture = False
            # Meeting has begun and/or finished, so can have an approvalSet.
            approvalSet = ApprovalSet.objects.filter(meeting=event)
            if len(approvalSet) == 0:
                approvalSet = ApprovalSet(meeting=event)
                approvalSet.save()
            elif len(approvalSet) == 1:
                approvalSet = approvalSet[0]
            else:
                # TODO: better choice of exception here would be sensible.
                raise Exception
            approvalSet.approvals
    return render_to_response('programming/meeting.html',
                              {
                                  'maintitle': event.title,
                                  'event': event,
                                  'extramessage': event.extramessage(request),
                                  'meetingInFuture': meetingInFuture,
                                  'approvalSet': approvalSet,
                              },
                              context_instance=RequestContext(request)
    )
