from ss.programming.models import Programmer

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None
    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class CurrentUser(object):
    __metaclass__ = Singleton
    _user = None
    _programmer = None
    def get_user(self):
        return self._user
    def set_user(self, value):
        self._user = value
    def del_user(self):
        self._user = None
        self._programmer = None
    user = property(get_user, set_user, del_user)
    def get_programmer(self):
        if self._programmer is None:
            if self._user is not None:
                self._programmer = Programmer.objects.get(user=self._user)
        return self._programmer
    def set_programmer(self, value):
        self._programmer = value
        self._user = value.user
    programmer = property(get_programmer, set_programmer)

class SSMiddleware(object):
    def process_request(self, request):
        user = CurrentUser()
        user.user = request.user
        #if request.path.split('/')[1] not in ['static', 'api']:
        #    if request.user.is_authenticated():
        #        allowed = True # TODO: This is where we need to think about who is allowed to approve events.
        #        currently = request.session.get('approvals-currently', False)
        #        meeting = request.session.get('approvals-meeting', None)
        #        if currently:
        #            meeting = Meeting.objects.get(id=meeting)
        #            meetingid = meeting.id
        #            messages.info(request, 'You are currently adding approvals for the <a href="%s">%s</a> on %s <a href="#" class="button stopapproving">Finish Approving</a>' % (
        #                meeting.get_absolute_url(),
        #                meeting.listHeading,
        #                meeting.shortDate,
        #            ), extra_tags='approving')
        #        else:
        #            meetingid = None
        #    else:
        #        allowed = False
        #        currently = False
        #        meetingid = None
        #    request.approvalsdata = {
        #            'allowed': allowed,
        #            'currently': currently,
        #            'meeting': meetingid,
        #        }
        return None
