

class XMLFormatter(object):

	def __init__(self, form=None):
		if form:
			self._format(form)
		else:
			self._title		= ""
			self._log_user	= ""
			self._text		= ""
	
	def _format(self, form):
		self._format_title(form)
		self._format_log_user(form)
		self._format_text(form)
	
	def _format_title(self, form):
		pass
	
	def _format_log_user(self, form):
		pass
	
	def _format_text(self, form):
		pass