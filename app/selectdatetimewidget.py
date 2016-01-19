from wtforms.widgets.core import Select, HTMLString, html_params
from datetime import datetime

class SelectDateTimeWidget(object):
	FORMAT_CHOICES = {
		'%d': [(x, str(x)) for x in range(1,32)],
		'%m': [(x, datetime.strptime(str(x), '%m').strftime('%b')) for x in range(1,13)],
		'%Y': [(x, str(x)) for x in range(2015,2017)],
		'%H': [(x, "{0:02d}".format(x)) for x in range(0,24)],
		'%M': [(x, "{0:02d}".format(x)) for x in range(0,60)],
		'%S': [(x, "{0:02d}".format(x)) for x in range(0,60)]
	}
	
	FORMAT_CLASSES = {
		'%d': 'select_date_day',
		'%m': 'select_date_month',
		'%Y': 'select_date_year',
		'%H': 'select_date_hour',
		'%M': 'select_date_minute',
		'%S': 'select_date_second'
	}
	
	def __call__(self, field, **kwargs):
		field_id = kwargs.pop('id', field.id)
		html = []
		allowed_formats = ['%d', '%m', '%Y', '%H', '%M', '%S']
		for format in field.format.split():
			if format in allowed_formats:	
				choices = self.FORMAT_CHOICES[format]
				id_suffix = format.replace('%', '-')
				id_current = field_id + id_suffix
				kwargs['class'] = self.FORMAT_CLASSES[format]
				try:
					del kwargs['placeholder']
				except:
					pass
				html.append('<select %s>' % html_params(name=field.name, id=id_current, **kwargs))
				if field.data:
					current_value = int(field.data.strftime(format))
				else:
					current_value = int(datetime.now().strftime(format))
				for value, label in choices:
					selected = (value == current_value)
					html.append(Select.render_option(value, label, selected))
				html.append('</select>')
			else:
				html.append(format)
				html.append('<input type="hidden" value="{0}" {1}></input>'.format(format, html_params(name=field.name, id=id_current, **kwargs)))
			html.append(' ')
			
		return HTMLString(''.join(html))