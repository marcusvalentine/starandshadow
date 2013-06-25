from django.conf.urls import *
from piston.resource import Resource
from ss.api.auth import DjangoAuthentication
from ss.api.handlers import PageHandler, SeasonHandler, FilmHandler, GigHandler, EventHandler, FestivalHandler, MeetingHandler, SeasonSelectHandler, ProgrammerSelectHandler, RatingSelectHandler, FilmformatSelectHandler, MeetingtypeSelectHandler, GraphicSelectHandler, PageSelectHandler, MenuSelectHandler, MeetingSelectHandler, MinutesHandler, DocumentHandler, DocumenttypeSelectHandler, approvalsSetMeeting, approveProgrammeItem, unapproveProgrammeItem, getApprovalData, getPrintProgrammeData, confirmItem

auth = DjangoAuthentication()

season_handler = Resource(SeasonHandler, authentication=auth)
film_handler = Resource(FilmHandler, authentication=auth)
gig_handler = Resource(GigHandler, authentication=auth)
event_handler = Resource(EventHandler, authentication=auth)
festival_handler = Resource(FestivalHandler, authentication=auth)
meeting_handler = Resource(MeetingHandler, authentication=auth)
document_handler = Resource(DocumentHandler, authentication=auth)

page_handler = Resource(PageHandler, authentication=auth)
minutes_handler = Resource(MinutesHandler, authentication=auth)

season_select_handler = Resource(SeasonSelectHandler, authentication=auth)
programmer_select_handler = Resource(ProgrammerSelectHandler, authentication=auth)
rating_select_handler = Resource(RatingSelectHandler, authentication=auth)
filmformat_select_handler = Resource(FilmformatSelectHandler, authentication=auth)
documenttype_select_handler= Resource(DocumenttypeSelectHandler, authentication=auth)
meetingtype_select_handler = Resource(MeetingtypeSelectHandler, authentication=auth)

graphic_select_handler = Resource(GraphicSelectHandler, authentication=auth)

meeting_select_handler = Resource(MeetingSelectHandler, authentication=auth)
page_select_handler = Resource(PageSelectHandler, authentication=auth)
menu_select_handler = Resource(MenuSelectHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^season/(?P<id>\d+)/?', season_handler),
    url(r'^season/', season_handler),
    url(r'^film/(?P<id>\d+)/?', film_handler),
    url(r'^film/', film_handler),
    url(r'^gig/(?P<id>\d+)/?', gig_handler),
    url(r'^gig/', gig_handler),
    url(r'^event/(?P<id>\d+)/?', event_handler),
    url(r'^event/', event_handler),
    url(r'^festival/(?P<id>\d+)/?', festival_handler),
    url(r'^festival/', festival_handler),
    url(r'^meeting/(?P<id>\d+)/?', meeting_handler),
    url(r'^meeting/', meeting_handler),
    url(r'^document/(?P<id>\d+)/?', document_handler),
    url(r'^document/', document_handler),

    url(r'^page/(?P<id>\d+)/?', page_handler),
    url(r'^page/', page_handler),
    url(r'^minutes/(?P<id>\d+)/?', minutes_handler),
    url(r'^minutes/', minutes_handler),

    url(r'^select/season/', season_select_handler),
    url(r'^select/programmer/', programmer_select_handler),
    url(r'^select/rating/', rating_select_handler),
    url(r'^select/filmformat/', filmformat_select_handler),
    url(r'^select/documenttype/', documenttype_select_handler),
    url(r'^select/meetingtype/', meetingtype_select_handler),

    url(r'^select/graphic/', graphic_select_handler),

    url(r'^select/meeting/', meeting_select_handler),
    url(r'^select/page/', page_select_handler),
    url(r'^select/menu/', menu_select_handler),

    url(r'^setmeeting/?$', approvalsSetMeeting),
    url(r'^approvaldata/?$', getApprovalData),
    url(r'^approveevent/?$', approveProgrammeItem),
    url(r'^unapproveevent/?$', unapproveProgrammeItem),
    url(r'^confirmitem/?$', confirmItem),
    url(r'^printprogramme/?$', getPrintProgrammeData),

)