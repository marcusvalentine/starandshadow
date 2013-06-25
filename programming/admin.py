from ss.programming.models import Programmer, Rating, Season, Film, Gig, Event, Festival, Meeting
from django.contrib import admin
from reversion.admin import VersionAdmin

class ProgrammerAdmin(VersionAdmin):
    list_display = ('name', 'homePhone', 'mobilePhone', 'email')
    search_fields = ['name']
    list_per_page = 40

class RatingAdmin(VersionAdmin):
    list_display = ('name',)
    list_per_page = 40
    prepopulated_fields = {"smallImage": ("largeImage",)}

class SeasonAdmin(VersionAdmin):
    list_display = ('title', 'startDate', 'endDate', 'programmer')
    list_filter = ['startDate', 'programmer']
    search_fields = ['title', 'summary']
    date_hierarchy = 'startDate'
    list_per_page = 40

class FilmAdmin(VersionAdmin):
    list_display = ('title', 'startDate', 'certificate', 'filmFormat', 'programmer')
    list_filter = ['startDate', 'programmer', 'certificate', 'filmFormat', 'season']
    search_fields = ['title', 'summary', 'director', 'season__title']
    date_hierarchy = 'startDate'
    list_per_page = 40
    
class GigAdmin(VersionAdmin):
    list_display = ('title', 'startDate', 'programmer')
    list_filter = ['startDate', 'programmer']
    search_fields = ['title', 'summary']
    date_hierarchy = 'startDate'
    list_per_page = 40

class EventAdmin(VersionAdmin):
    list_display = ('title', 'startDate', 'programmer')
    list_filter = ['startDate', 'programmer']
    search_fields = ['title', 'summary']
    date_hierarchy = 'startDate'
    list_per_page = 40

class FestivalAdmin(VersionAdmin):
    list_display = ('title', 'startDate', 'endDate', 'programmer')
    list_filter = ['startDate', 'programmer']
    search_fields = ['title', 'summary']
    date_hierarchy = 'startDate'
    filter_horizontal = ['films', 'gigs', 'events']
    list_per_page = 40

class MeetingAdmin(VersionAdmin):
    list_display = ('title', 'startDate')
    list_filter = ['startDate']
    search_fields = ['title']
    date_hierarchy = 'startDate'
    list_per_page = 40

admin.site.register(Rating, RatingAdmin)
admin.site.register(Programmer, ProgrammerAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Gig, GigAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Festival, FestivalAdmin)
admin.site.register(Meeting, MeetingAdmin)