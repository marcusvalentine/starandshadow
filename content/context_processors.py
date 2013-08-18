from ss.content.models import Menu
from django.contrib import messages


def menus(request):
    menus = ''
    menus += '''<section class="row">
    <header><h3>About Us</h3></header>
    <ul class="nav nav-list">
        %s
        <li><a href="/accounts/login/">Login</a></li>
    </ul>
</section>''' % Menu.objects.get(id=2).asLi()
    menus += '''<section class="row">
    <header><h3>What's On</h3></header>
    <ul class="nav nav-list">
        <li><a href="/on/today/">Today</a></li>
        <li><a href="/on/thisweek/">This Week</a></li>
        <li><a href="/on/nextweek/">Next Week</a></li>
        <li><a href="/on/thismonth/">This Month</a></li>
        <li><a href="/on/nextmonth/">Next Month</a></li>
    </ul>
</section>'''
    return {'menus': menus, 'request': request, }


def authenticated(request):
    if request.user.is_authenticated():
        messages.info(request,
                      'Logged in as %s <a class="button" href="/accounts/logout/">Logout</a>' % request.user.username)
        return {
            'authenticated': True,
            'user': request.user
        }
    else:
        return {
            'authenticated': False,
            'user': None
        }
