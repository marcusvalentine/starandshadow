Problems after move:

Pages have eventtype -> schema.org problem
Change notifications don't seem to happen for eventtypes

------------------

Install:

Install Python 2.7, 64 bit
Install MySQL-python, 64 bit (http://www.lfd.uci.edu/~gohlke/pythonlibs/, MySQL-python-1.2.4.win-amd64-py2.7.‌exe)
Install Pillow, 64 bit (http://www.lfd.uci.edu/~gohlke/pythonlibs/, Pillow-2.0.0.win-amd64-py2.7.‌exe)
Install distribute and pip, through pycharm
pip install virtualenv
virtualenv --system-site-packages PATH_TO_PROJECT\venv
PATH_TO_PROJECT\venv\scripts\activate
pip install -r requirements.txt

Get DB Dump
import db
Flush thumbnail cache ("DELETE FROM thumbnail_kvstore")
ss migrate fileupload
ss migrate organisation
ss migrate programming

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
