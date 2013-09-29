from organisation.models import Minutes, BoxOfficeReturn, PrintProgramme
from django.contrib import admin
from reversion.admin import VersionAdmin


class MinutesAdmin(VersionAdmin):
    list_display = ('listHeading', )
    search_fields = ['listHeading', ]
    list_per_page = 40


class BoxOfficeReturnAdmin(VersionAdmin):
    pass


class PrintProgrammeAdmin(VersionAdmin):
    pass


admin.site.register(Minutes, MinutesAdmin)
admin.site.register(BoxOfficeReturn, BoxOfficeReturnAdmin)
admin.site.register(PrintProgramme, PrintProgrammeAdmin)