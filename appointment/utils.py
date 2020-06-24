from datetime import datetime, timedelta
from calendar import HTMLCalendar
from appointment.models import Appointment

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(event_date__day=day)
		d = ''
		for event in events_per_day:
			d += f'<a class="fc-day-grid-event fc-h-event fc-event fc-start fc-end bg-info fc-draggable" href="{event.get_absolute_url} event.pk"><div class="fc-content"><span class="fc-time">{event.time} </span><span class="fc-title">{event.user.first_name}</span></div></a>'

		if day != 0:
			return f"<td class='fc-event-container'><span class='fc-day-number'>{day}</span>{d}</td>"
            
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<div class="fc-content-skeleton" ><table><td class="fc-day-top fc-sun fc-past"  "><tr><td style="height: 120px;"> {week} </td></tr></table></div>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Appointment.objects.filter(event_date__year=self.year, event_date__month=self.month).order_by('time')

		cal = f'<tbody class="fc-body">'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal