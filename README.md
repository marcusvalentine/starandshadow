Install:

Install Python 2.7, 64 bit
Install MySQL-python, 64 bit (http://www.lfd.uci.edu/~gohlke/pythonlibs/, MySQL-python-1.2.4.win-amd64-py2.7.‌exe)
Install Pillow, 64 bit (http://www.lfd.uci.edu/~gohlke/pythonlibs/, Pillow-2.0.0.win-amd64-py2.7.‌exe)
Install distribute and pip, through pycharm
pip install virtualenv
virtualenv --system-site-packages PATH_TO_PROJECT\venv
PATH_TO_PROJECT\venv\scripts\activate
pip install django # Django 1.5.1
pip install bleach # bleach 1.2.2
pip install python-dateutil # python-dateutil 2.1
pip install django-registration # django-registration 1.0
pip install django-reversion # django-reversion 1.7.1
pip install sorl-thumbnail # sorl-thumbnail 11.12
pip install South # South 0.8.1
pip install django-compressor # django-compressor 1.3
pip install django-tastypie # tastypie 0.9.15
pip install pytz # pytz 2013b
pip install BeautifulSoup # BeautifulSoup 3.2.1

Get DB Dump
s/ENGINE=MyISAM/ENGINE=InnoDB/g
import db
Flush thumbnail cache ("DELETE FROM thumbnail_kvstore")
INSERT INTO south_migrationhistory SET id=21,app_name="fileupload",migration="0002_auto__add_field_picture_modified",applied="2013-06-29 23:00:00";
May need to bodge South: http://south.aeracode.org/ticket/1227
ss migrate fileupload
ss migrate organisation
ss migrate programming
Deduplicate images (see below)

JavaScript libs:

static/js/libs:
    jquery 1.10.1
    jquery-ui custom, with humanity theme 1.10.3
    knockout.js 2.2.1
    knockout.mapping-2.4.1.js


Copy images from whereever to the various image folders.

Edit an item and poke the image selector to pre-populate the image cache.

-------------------

TODO:

Add a notes field to all events.

images moved from static/content to static/events and static/import to static/events

Thoughts:

Add straight from month list.
landing page should be the "this month" page
symbols for event types?
onhover highlighting similar events
"upcoming highlights" page
Tooltips for info on "confirmed" and "approved" icons.
Approvals logic needs finishing.

Make people aware of:

Distinction between Approved and Confirmed.

-----------------------

Deduplication of images:

UPDATE programming_event
JOIN (
    SELECT g.id id, g.title title, p.id pictureid, p.slug pictureslug, q.id minid
    FROM programming_event g
    JOIN (
        SELECT id,slug
        FROM fileupload_picture
    ) p ON g.picture_id = p.id
    JOIN (
        SELECT id,slug
        FROM fileupload_picture
    ) q ON p.slug = q.slug
    GROUP BY p.slug
    HAVING COUNT(*) > 1
) q on programming_event.id = q.id
SET programming_event.picture_id = q.minid;

UPDATE programming_festival
JOIN (
    SELECT g.id id, g.title title, p.id pictureid, p.slug pictureslug, q.id minid
    FROM programming_festival g
    JOIN (
        SELECT id,slug
        FROM fileupload_picture
    ) p ON g.picture_id = p.id
    JOIN (
        SELECT id,slug
        FROM fileupload_picture
    ) q ON p.slug = q.slug
    GROUP BY p.slug
    HAVING COUNT(*) > 1
) q on programming_festival.id = q.id
SET programming_festival.picture_id = q.minid;

UPDATE programming_film
JOIN (
    SELECT g.id id, g.title title, p.id pictureid, p.slug pictureslug, q.id minid
    FROM programming_film g
    JOIN (
        SELECT id,slug
        FROM fileupload_picture
    ) p ON g.picture_id = p.id
    JOIN (
        SELECT id,slug
        FROM fileupload_picture
    ) q ON p.slug = q.slug
    GROUP BY p.slug
    HAVING COUNT(*) > 1
) q on programming_film.id = q.id
SET programming_film.picture_id = q.minid;

UPDATE programming_gig
JOIN (
    SELECT g.id id, g.title title, p.id pictureid, p.slug pictureslug, q.id minid
    FROM programming_gig g
    JOIN (
        SELECT id,slug
        FROM fileupload_picture
    ) p ON g.picture_id = p.id
    JOIN (
        SELECT id,slug
        FROM fileupload_picture
    ) q ON p.slug = q.slug
    GROUP BY p.slug
    HAVING COUNT(*) > 1
) q on programming_gig.id = q.id
SET programming_gig.picture_id = q.minid;

UPDATE programming_season
JOIN (
    SELECT g.id id, g.title title, p.id pictureid, p.slug pictureslug, q.id minid
    FROM programming_season g
    JOIN (
        SELECT id,slug
        FROM fileupload_picture
    ) p ON g.picture_id = p.id
    JOIN (
        SELECT id,slug
        FROM fileupload_picture
    ) q ON p.slug = q.slug
    GROUP BY p.slug
    HAVING COUNT(*) > 1
) q on programming_season.id = q.id
SET programming_season.picture_id = q.minid;

DELETE fileupload_picture.*
FROM fileupload_picture
LEFT JOIN (
    SELECT MIN(id) minid
    FROM fileupload_picture
    GROUP BY slug
) g ON fileupload_picture.id = g.minid
WHERE g.minid is NULL;
