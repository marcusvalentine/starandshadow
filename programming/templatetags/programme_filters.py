from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import bleach
from BeautifulSoup import BeautifulSoup
import re
from sorl.thumbnail import get_thumbnail
from fileupload.models import Picture
from django.utils.formats import date_format

register = template.Library()


@register.filter
@stringfilter
def sanitize(value):
    parenty = re.compile(r'"(\.\.\/)+', re.MULTILINE | re.IGNORECASE)
    value = parenty.sub(r'"/', value)
    #oldstyle = re.compile(r'<b>(.*?)</b>', re.MULTILINE | re.IGNORECASE)
    #value = oldstyle.sub(r'<strong>\1</strong>', value)
    #oldstyle = re.compile(r'<i>(.*?)</i>', re.MULTILINE | re.IGNORECASE)
    #value = oldstyle.sub(r'<em>\1</em>', value)
    styletag = re.compile(r'<style(.*?)</style>', re.MULTILINE | re.IGNORECASE)
    value = styletag.sub(r'', value)
    tags = [
        'div',
        'span',
        'p',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'ul',
        'ol',
        'li',
        'dl',
        'dt',
        'dd',
        'a',
        'strong',
        'b',
        'em',
        'i',
        'hr',
        'abbr',
        'acronym',
        'blockquote',
        'code',
        'img',
        'iframe',
    ]
    attributes = {
        '*': ['class', ],
        'a': ['href', 'title', ],
        'abbr': ['title', ],
        'acronym': ['title', ],
        'img': ['height', 'width', 'alt', 'title', 'src'],
        'iframe': ['height', 'width', 'src', 'frameborder', 'allowfullscreen'],
    }
    value = bleach.clean(value, tags=tags, attributes=attributes, strip=True)
    #value = bleach.linkify(value, nofollow=False) # this breaks youtube iframes, which is a shame.
    soup = BeautifulSoup(value)
    for img in soup.findAll('img'):
        try:
            if img['src'][0] != '/':
                urlelements = img['src'].split('/')
                if urlelements[2] == 'www.starandshadow.org.uk' or urlelements[2] == '127.0.0.1:8000':
                    img['src'] = img['src'].split(urlelements[2])[1]
                else:
                    img['src'] = '/static/img/import/%s?origsrc=%s' % (img['src'].split('/')[-1], img['src'])
        except KeyError:
            img.extract()
    for mso in soup.findAll(True, "MsoNormal"):
        del (mso['class'])
    for tag in soup.findAll(
            lambda tag: (tag.name == 'span' or tag.name == 'p' or tag.name == 'div') and tag.find(True) is None and (
                            tag.string is None or tag.string.strip() == '')):
        tag.extract()
    value = soup.renderContents().decode('utf8')
    dotty = re.compile(r'\.{2,}', re.MULTILINE | re.IGNORECASE)
    value = dotty.sub(r'&hellip;', value)
    liny = re.compile(r'[_-]{2,}', re.MULTILINE | re.IGNORECASE)
    value = liny.sub(r'<hr>', value)
    starry = re.compile(r'\*{1,}([^\*]*)\*{1,}', re.MULTILINE | re.IGNORECASE)
    value = starry.sub(r'<strong>\1</strong>', value)
    return mark_safe(value)


MDPROPS = {
    'title': 'name',
    'startDate': '',
    'startTime': '',
    'startDateTime': 'startDate',
    'endDate': '',
    'endTime': '',
    'endDateTime': 'endDate',
    'length': 'duration',
    'summary': 'description',
    'body': 'about',
    'director': 'name',
    'year': 'copyrightyear',
    'lang': 'inLanguage',
    'country': '',
    'certificate': 'contentRating',
    'filmFormat': '',
    'season': 'superEvent',
    'picture': 'image',
    'notes': '',
    'programmer': '',
    'approval': '',
    'confirmed': '',
    'private': '',
    'featured': '',
    'website': '',
    'films': '',
    'gigs': '',
    'events': '',
    'festivals': '',
    # docs:
    'author': 'author',
    'source': 'author',
    'created': 'dateCreated',
    'articleBody': 'articleBody',
    # minutes:
    'meeting': 'title',
    # pages
    'slug': '',
    'parent': '',
    'order': '',
}


@register.filter
def md_meta(event, fieldName=None):
    if fieldName is None:
        return ''
    else:
        return mark_safe(
            '''<meta itemprop="%s" content="%s" data-bind="attr:{content:%s}">''' % (
                MDPROPS[fieldName],
                getattr(event, fieldName),
                fieldName,
            )
        )


@register.filter
def md(event, fieldName=None):
    if fieldName is None:
        if event.typeName == 'document' or event.typeName == 'minutes':
            itemtype = 'http://schema.org/Article'
            itemtypeclass = 'documenttype'
        else:
            itemtype = 'http://schema.org/Event'
            itemtypeclass = 'eventtype'
        return mark_safe(
            '''<div '''
            '''id="%s-%s" '''
            '''class="%s editthis" '''
            '''itemscope '''
            '''itemtype="%s" '''
            '''data-modeltype="%s" '''
            '''data-modelid="%s" '''
            '''data-apiobjecturl="%s">'''
            % (
                event.typeName.lower(),
                event.id,
                itemtypeclass,
                itemtype,
                event.typeName,
                event.id,
                event.api_object_url,
            ))
    else:
        if MDPROPS[fieldName] == '':
            itemprop = ''
        else:
            itemprop = ' itemprop="%s"' % MDPROPS[fieldName]
            #     return '<span itemprop="name" data-bind="text:title">{{ maintitle|title }}</span>'
        # elif fieldName == 'festivals':
        #     festivals = []
        #     for festival in event.festival_set.all():
        #         festivals.append(
        #             '''<h3 itemprop="superEvent" itemscope itemtype="http://schema.org/Event">'''
        #             '''Part of <a itemprop="url" href="%s"><span itemprop="name">%s</span></a>'''
        #             '''</h3>''' % (
        #                 festival.get_absolute_url(),
        #                 festival,
        #             ))
        #     return mark_safe(''.join(festivals))
        if fieldName == 'startDate':
            return mark_safe(
                '''<time class="%s"%s datetime="%s" data-bind="attr:{datetime:startDateTime()},text:displayStart()">%s</time>'''
                % (
                    fieldName,
                    itemprop,
                    event.startDate,
                    event.displayStart,
                ))
        elif fieldName == 'startDateTime':
            return mark_safe(
                '''<time class="%s"%s datetime="%s" data-bind="attr:{datetime:startDateTime()},text:displayStart()">%s</time>'''
                % (
                    fieldName,
                    itemprop,
                    event.startDateTime,
                    event.displayStart,
                ))
        elif fieldName == 'endDateTime':
            return mark_safe(
                '''<time class="%s"%s datetime="%s" data-bind="attr:{datetime:endDateTime()},text:displayEnd()">%s</time>'''
                % (
                    fieldName,
                    itemprop,
                    event.endDateTime,
                    event.displayEnd,
                ))
        elif fieldName == 'endDate':
            return mark_safe(
                '''<time class="%s"%s datetime="%s" data-bind="attr:{datetime:endDateTime()},text:displayEnd()">%s</time>'''
                % (
                    fieldName,
                    itemprop,
                    event.endDate,
                    event.displayEnd,
                ))
        elif fieldName == 'length':
            return mark_safe(
                '''<time class="%s"%s datetime="%s" data-bind="attr:{datetime:isolength()},text:lengthLabel()">%s</time>'''
                % (
                    fieldName,
                    itemprop,
                    event.isolength,
                    event.length,
                ))
        elif fieldName == 'summary':
            return ''
        elif fieldName == 'body' or fieldName == 'articleBody':
            return mark_safe(
                '''<div class="%s"%s data-fieldname="body" data-bind="htmlValue:body">%s</div>'''
                % (
                    fieldName,
                    itemprop,
                    #event.body,
                    sanitize(event.body),
                ))
        elif fieldName == 'director':
            return mark_safe(
                '''<span itemprop="%s" itemscope itemtype="http://schema.org/Person"><span class="%s"%s data-bind="text:%s">%s</span></span>'''
                % (
                    fieldName,
                    fieldName,
                    itemprop,
                    fieldName,
                    getattr(event, fieldName),
                ))
        elif fieldName == 'year':
            if event.year:
                yearb = '(%s)' % event.year
            else:
                yearb = ''
            return mark_safe(
                '''<span class="%s"%s content="%s" data-bind="attr:{content:year}, text: showYear()"> %s</span>'''
                % (
                    fieldName,
                    itemprop,
                    event.year,
                    yearb
                ))
        elif fieldName == 'certificate' or fieldName == 'filmFormat' or fieldName == 'approval' or fieldName == 'programmer':
            return mark_safe(
                '''<span class="%s"%s data-bind="text:%s">%s</span>'''
                % (
                    fieldName,
                    itemprop,
                    'selectedLabel' + fieldName,
                    getattr(event, fieldName),
                ))
        elif fieldName == 'season':
            return mark_safe(
                '''Part of the <a href="%s" class="%s"%s data-bind="attr:{href:%s},text:%s">%s</a> Season'''
                % (
                    getattr(event, fieldName).get_absolute_url(),
                    fieldName,
                    itemprop + ' itemscope itemtype="http://schema.org/Event"',
                    'selectedLink' + fieldName,
                    'selectedLabel' + fieldName,
                    getattr(event, fieldName),
                ))
        elif fieldName == 'meeting':
            return mark_safe(
                '''Minutes of <a href="%s" class="%s"%s data-bind="attr:{href:%s},text:%s">%s</a>'''
                % (
                    getattr(event, fieldName).get_absolute_url(),
                    fieldName,
                    itemprop + ' itemscope itemtype="http://schema.org/Event"',
                    'selectedLink' + fieldName,
                    'selectedLabel' + fieldName,
                    event.meeting.longHeading,
                ))
        elif fieldName == 'picture':
            if event.picture is None:
                event.picture = Picture.objects.get(id=789)
            return mark_safe(
                '''<img class="%s pull-right img-responsive"%s'''
                ''' data-fieldname="picture"'''
                ''' src="%s"'''
                ''' width="%s"'''
                ''' height="%s"'''
                ''' data-src="%s"'''
                ''' data-width="%s"'''
                ''' data-height="%s"'''
                ''' data-toggle="modal"'''
                ''' data-target="#img-picture-%s"'''
                ''' alt=""'''
                ''' data-bind="attr: {'''
                ''' src: pictureData().displaySrc,'''
                ''' width: pictureData().displayWidth,'''
                ''' height: pictureData().displayHeight,'''
                ''' 'data-src': pictureData().src,'''
                ''' 'data-width': pictureData().width,'''
                ''' 'data-height': pictureData().height'''
                ''' }" />'''
                '''<div class="modal " id="img-picture-%s">'''
                '''    <div class="modal-dialog">'''
                '''        <div class="modal-content">'''
                '''            <div class="modal-header">'''
                '''                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">'''
                '''                    &times;'''
                '''                </button>'''
                '''            </div>'''
                '''            <div class="modal-body">'''
                '''                <img src="%s" class="img-responsive" alt="" data-bind="attr: {src: pictureData().displaySrc}">'''
                '''            </div>'''
                '''        </div>'''
                '''    </div>'''
                '''</div>'''
                % (
                    fieldName,
                    itemprop,
                    event.picture.displaySrc,
                    event.picture.displayWidth,
                    event.picture.displayHeight,
                    event.picture.src,
                    event.picture.width,
                    event.picture.height,
                    event.picture.id,
                    event.picture.id,
                    event.picture.src,
                ))
        # elif fieldName == 'notes':
        # elif fieldName == 'approval':
        # elif fieldName == 'confirmed':
        # elif fieldName == 'private':
        # elif fieldName == 'featured':
        elif fieldName == 'website':
            return mark_safe(
                '''<div itemprop="subEvents" itemscope itemtype="http://schema.org/Event" data-bind="visible:websiteVisible">'''
                '''    <meta itemprop="name" content="%s">'''
                '''    <p>External Website: <a itemprop="url" data-bind="attr:{href:website},text:website" href="%s">%s</a></p>'''
                '''</div>'''
                % (
                    event.title,
                    event.website,
                    event.website,
                ))
        # elif fieldName == 'films':
        # elif fieldName == 'gigs':
        # elif fieldName == 'events':
        elif fieldName == 'festivals':
            return ''
        else:
            try:
                return mark_safe(
                    '''<span class="%s"%s data-bind="text:%s">%s</span>'''
                    % (
                        fieldName,
                        itemprop,
                        fieldName,
                        getattr(event, fieldName),
                    ))
            except AttributeError:
                return mark_safe('''<span>Error</span>''')

