from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from programming.models import Programmer, Rating, Season, Film, Gig, Event, Festival, Meeting
from organisation.models import Minutes, BoxOfficeReturn, LogItem
from organisation.forms import SeasonAdminForm, FilmAdminForm, GigAdminForm, EventAdminForm, FestivalAdminForm, MeetingAdminForm, SeasonForm, FilmForm, GigForm, EventForm, FestivalForm, MeetingForm, ProgrammerForm, MinutesForm, BoxOfficeReturnForm
from lib.utils import ssDate, Prog
from django.utils.timezone import datetime
import calendar
from django.contrib.auth.decorators import login_required
from decimal import *


@login_required
def reportIndex(request):
    thisYear = datetime.now().year
    thisMonth = datetime.now().month
    periods = [
        [(year, x, calendar.month_name[x]) for year in range(thisYear - 4, thisYear + 6)]
        for x in range(1, 13)
    ]
    return render_to_response('organisation/reportIndex.html',
                              {
                                  'maintitle': 'Programme',
                                  'periods': periods,
                                  'thisYear': thisYear,
                                  'thisMonth': thisMonth,
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def returnReportIndex(request):
    thisYear = datetime.now().year
    thisMonth = datetime.now().month
    periods = [
        [(year, x, calendar.month_name[x]) for year in range(thisYear - 4, thisYear + 6)]
        for x in range(1, 13)
    ]
    return render_to_response('organisation/returnReportIndex.html',
                              {
                                  'maintitle': 'Box Office Returns',
                                  'periods': periods,
                                  'thisYear': thisYear,
                                  'thisMonth': thisMonth,
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def itemEdit(request, item, ItemForm, ItemAdminForm, template='edit.html', viewAfter=True):
    if request.user.is_staff:
        if request.method == 'POST':
            form = ItemAdminForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                if viewAfter:
                    return redirect(item.get_absolute_url())
        else:
            form = ItemAdminForm(instance=item)
    elif request.user == item.programmer.user:
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                if viewAfter:
                    return redirect(item.get_absolute_url())
        else:
            form = ItemForm(instance=item)
    else:
        form = False
    return render_to_response('organisation/%s' % template,
                              {
                                  'maintitle': 'Edit / Add %s' % item._meta.object_name,
                                  'item': item,
                                  'form': form,
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def seasonEdit(request, eventId=None):
    if eventId is None:
        item = Season()
        item.programmer = Programmer.objects.get(user=request.user)
    else:
        item = get_object_or_404(Season, id=eventId)
    return itemEdit(request, item, SeasonForm, SeasonAdminForm, 'editSeason.html')


@login_required
def filmEdit(request, eventId=None):
    if eventId is None:
        item = Film()
        item.programmer = Programmer.objects.get(user=request.user)
        item.certificate = Rating.objects.get(pk=1)
        item.season = Season.objects.get(pk=2)
    else:
        item = get_object_or_404(Film, id=eventId)
    return itemEdit(request, item, FilmForm, FilmAdminForm, 'editFilm.html')


@login_required
def gigEdit(request, eventId=None):
    if eventId is None:
        item = Gig()
        item.programmer = Programmer.objects.get(user=request.user)
    else:
        item = get_object_or_404(Gig, id=eventId)
    return itemEdit(request, item, GigForm, GigAdminForm, 'editGig.html')


@login_required
def eventEdit(request, eventId=None):
    if eventId is None:
        item = Event()
        item.programmer = Programmer.objects.get(user=request.user)
    else:
        item = get_object_or_404(Event, id=eventId)
    return itemEdit(request, item, EventForm, EventAdminForm, 'editEvent.html')


@login_required
def festivalEdit(request, eventId=None):
    if eventId is None:
        item = Festival()
        item.programmer = Programmer.objects.get(user=request.user)
    else:
        item = get_object_or_404(Festival, id=eventId)
    return itemEdit(request, item, FestivalForm, FestivalAdminForm, 'editFestival.html')


@login_required
def meetingEdit(request, eventId=None):
    if eventId is None:
        item = Meeting()
    else:
        item = get_object_or_404(Meeting, id=eventId)
    return itemEdit(request, item, MeetingForm, MeetingAdminForm)


@login_required
def minutesEdit(request, eventId=None, forMeeting=None):
    if eventId is None:
        if forMeeting is None:
            item = Minutes()
        else:
            item = Minutes(meeting=get_object_or_404(Meeting, id=forMeeting))
    else:
        item = get_object_or_404(Minutes, id=eventId)
    return itemEdit(request, item, MinutesForm, MinutesForm, viewAfter=True)


@login_required
def minutesAdd(request, forMeeting=None):
    minutes = Minutes(meeting=get_object_or_404(Meeting, id=forMeeting))
    minutes.save()
    return redirect(reverse('view-minutes', kwargs={'minutesId': minutes.pk}))


@login_required
def minutesView(request, minutesId=None):
    minutes = get_object_or_404(Minutes, id=minutesId)
    return render_to_response('organisation/minutes.html',
                              {
                                  'maintitle': minutes.listHeading,
                                  'event': minutes,
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def minutesList(request):
    minutess = Minutes.objects.all()
    return render_to_response('organisation/minutesList.html',
                              {
                                  'maintitle': 'Minutes',
                                  'minutess': minutess,
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def meetingsReport(request, year=None):
    if year is None:
        year = datetime.now().year
    cal = ssDate(size='year', year=year)
    prog = Prog(cal=cal, types=[Meeting.objects, ])
    return render_to_response('organisation/meetingReport.html',
                              {
                                  'maintitle': 'Meetings %s' % year,
                                  'cal': cal,
                                  'prog': prog.byDate(trimmed=True),
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def monthReport(request, year, month):
    cal = ssDate(year=year, month=month, size='month')
    prog = Prog(cal=cal, all=True)
    return render_to_response('organisation/report.html',
                              {
                                  'maintitle': cal.strftime("%B %Y"),
                                  'cal': cal,
                                  'prog': prog.byDate(),
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def returnEdit(request, eventId=None, filmId=None):
    if eventId is None:
        if filmId is None:
            ret = BoxOfficeReturn()
        else:
            ret = BoxOfficeReturn(film=get_object_or_404(Film, id=filmId))
    else:
        ret = get_object_or_404(BoxOfficeReturn, id=eventId)
    if request.method == 'POST':
        form = BoxOfficeReturnForm(request.POST, instance=ret)
        if form.is_valid():
            form.save()
            return redirect(
                reverse('return-report', kwargs={'year': ret.film.startDate.year, 'month': ret.film.startDate.month}))
    else:
        form = BoxOfficeReturnForm(instance=ret)
    return render_to_response('organisation/editReturn.html',
                              {
                                  'maintitle': 'Edit Box Office Return',
                                  'return': ret,
                                  'form': form,
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def returnReport(request, year, month):
    cal = ssDate(year=year, month=month, size='month')
    prog = Prog(types=[Film.objects, ], cal=cal)
    prog = prog.byDate(trimmed=True)
    totals = {
        'newMembers': 0,
        'membershipTake': Decimal('0.00'),
        'normalTickets': 0,
        'normalTake': Decimal('0.00'),
        'concessionTickets': 0,
        'concessionTake': Decimal('0.00'),
        'ticketTake': Decimal('0.00'),
        'totalTake': Decimal('0.00'),
    }
    for day, events in prog:
        for event in events:
            try:
                ret = event.boxofficereturn_set.all()[0]
                totals['newMembers'] += ret.newMembers
                totals['membershipTake'] += ret.membershipTake()
                totals['normalTickets'] += ret.normalTickets
                totals['normalTake'] += ret.normalTake()
                totals['concessionTickets'] += ret.concessionTickets
                totals['concessionTake'] += ret.concessionTake()
                totals['ticketTake'] += ret.ticketTake()
                totals['totalTake'] += ret.totalTake()
            except IndexError:
                pass
    return render_to_response('organisation/returnReport.html',
                              {
                                  'maintitle': 'Box Office Returns ' + cal.strftime("%B %Y"),
                                  'cal': cal,
                                  'prog': prog,
                                  'totals': totals,
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def monthReportText(request, year, month):
    cal = ssDate(year=year, month=month, size='month')
    prog = Prog(cal=cal, all=True)
    return render_to_response('organisation/reportText.html',
                              {
                                  'maintitle': cal.strftime("%B %Y"),
                                  'cal': cal,
                                  'prog': prog.byDate(),
                              },
                              context_instance=RequestContext(request),
                              mimetype='text/plain; charset="utf-8"',
    )


@login_required
def volunteerIndex(request):
    volunteers = Programmer.objects.all()
    return render_to_response('organisation/volunteerIndex.html',
                              {
                                  'maintitle': 'Volunteers',
                                  'volunteers': volunteers,
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def volunteerEdit(request, volunteerId):
    volunteer = get_object_or_404(Programmer, user=volunteerId)
    if request.user.is_staff or volunteer.user.id == int(volunteerId):
        if request.method == 'POST':
            form = ProgrammerForm(request.POST, request.FILES, instance=volunteer)
            if form.is_valid():
                form.save()
                return redirect(volunteer.get_absolute_url())
        else:
            form = ProgrammerForm(instance=volunteer)
    else:
        form = False
    return render_to_response('organisation/volunteerEdit.html',
                              {
                                  'maintitle': volunteer.name,
                                  'volunteer': volunteer,
                                  'form': form,
                              },
                              context_instance=RequestContext(request)
    )


@login_required
def volunteerProfile(request, volunteerId):
    volunteer = get_object_or_404(Programmer, user=volunteerId)
    prog = Prog(volunteer=volunteer, all=True, reverse=True)
    return render_to_response('organisation/volunteerProfile.html',
                              {
                                  'maintitle': volunteer.name,
                                  'volunteer': volunteer,
                                  'prog': prog.byDate(trimmed=True),
                              },
                              context_instance=RequestContext(request)
    )

@login_required
def volunteerMe(request):
    return volunteerProfile(request, request.user.id)

@login_required
def changeLog(request):
    loglines = LogItem.objects.all()
    return render_to_response('organisation/changelog.html',
                              {
                                  'maintitle': 'Change Log',
                                  'loglines': loglines,
                              },
                              context_instance=RequestContext(request)
    )