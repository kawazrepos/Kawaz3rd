

from icalendar import Calendar
from icalendar import Event as CalEvent
from icalendar import vCalAddress, vText, vDatetime
from django.conf import settings
from django.contrib.sites.models import Site

def generate_ical(object):
    cal = Calendar()
    cal['PRODID'] = 'Kawaz'
    cal['VERSION'] = '2.0'
    site = Site.objects.get(pk=settings.SITE_ID)

    event = CalEvent()
    event['summary'] = object.title
    event['description'] = object.body
    event['class'] = 'PUBLIC' if object.pub_state == 'public' else 'PRIVATE'
    if object.category:
        event['categories'] = object.category.label
    event['dtstamp'] = vDatetime(object.created_at)
    if object.place:
        event['location'] = object.place
    event['dtstart'] = vDatetime(object.period_start).to_ical()
    if object.period_end:
        event['dtend'] = vDatetime(object.period_end).to_ical()

    def create_vaddress(user):
        va = vCalAddress('MAILTO:{}'.format(user.email))
        va.params['cn'] = vText(user.nickname)
        va.params['ROLE'] = vText(user.role)
        return va

    organizer = create_vaddress(object.organizer)
    event['organizer'] = organizer
    event['URL'] = 'http://{}{}'.format(site.domain, object.get_absolute_url())

    for attendee in object.attendees.all():
        event.add('attendee', create_vaddress(attendee), encode=0)

    cal.add_component(event)

    return cal
