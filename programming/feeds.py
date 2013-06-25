from django.contrib.syndication.views import Feed
from ss.lib.utils import ssDate, Prog
from datetime import date, timedelta

class listPeriodFeed(Feed):
    def get_object(self, request, *args, **kwargs):
        return ssDate(None, **kwargs)
    def title(self, cal):
        return 'Star And Shadow Events %s to %s' % (cal.startDate(), cal.endDate())
    def description(self, cal):
        return 'Star And Shadow Events %s to %s' % (cal.startDate(), cal.endDate())
    def link(self, cal):
        return cal.onUrl() + 'feed/'
    def items(self, cal):
        return [item for item in Prog(cal=cal).flat() if item.approved]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        try:
            return item.summary
        except AttributeError:
            return item.title

class listTodayFeed(listPeriodFeed):
    def get_object(self, request, *args, **kwargs):
        return ssDate(date.today(), size='day')
class listWeekFeed(listPeriodFeed):
    def get_object(self, request, *args, **kwargs):
        return ssDate(date.today(), size='week')
class listNextWeekFeed(listPeriodFeed):
    def get_object(self, request, *args, **kwargs):
        return ssDate(date.today() + timedelta(days=7), size='week')
class listMonthFeed(listPeriodFeed):
    def get_object(self, request, *args, **kwargs):
        return ssDate(date.today(), size='month')
class listNextMonthFeed(listPeriodFeed):
    def get_object(self, request, *args, **kwargs):
        return ssDate(date.today() + timedelta(days=30), size='month')
