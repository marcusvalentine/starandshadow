from content.models import Menu,Page,News,Document
from django.contrib import admin
from reversion.admin import VersionAdmin

class MenuAdmin(VersionAdmin):
    list_display = ('linkText', 'title')
    list_per_page = 40
    prepopulated_fields = {'linkText': ('title',)}

class PageAdmin(VersionAdmin):
    list_display = ('linkText', 'title', 'parent', 'order')
    list_filter = ('parent',)
    search_fields = ['title', 'body']
    list_per_page = 50
    prepopulated_fields = {"linkText": ("title",)}

class NewsAdmin(VersionAdmin):
    #list_display = ('title', 'publishDate', 'withdrawDate', 'current')
    #list_filter = ('publishDate', 'withdrawDate')
    search_fields = ['title', 'summary', 'body', 'caption']
    #date_hierarchy = 'publishDate'
    list_per_page = 40

class DocumentAdmin(VersionAdmin):
    list_display = ('title', 'type', 'author')
    list_filter = ('type', 'author')
    search_fields = ['title', 'source', 'summary', 'author', 'body']
    list_per_page = 40

admin.site.register(Menu,MenuAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Document,DocumentAdmin)
