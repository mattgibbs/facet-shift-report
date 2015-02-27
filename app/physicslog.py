import requests, re, os.path, mimetypes
from datetime import datetime
class Entry:
	def __init__(self, title = None, author = None, text = None):
		self.text = text
		self.title = title
		self.author = author
		self.timestamp = None
		self.file_path = None
	
	def to_dict(self):
		entry_dict = dict()
		entry_dict['text'] = ('',self.text)
		entry_dict['author'] = ('',self.author)
		entry_dict['title'] = ('',self.title)
		entry_dict['keywords'] = ('', 'Other')
		entry_dict['experts'] = ('','')
		entry_dict['date'] = ('',self.timestamp.strftime('%m/%d/%Y'))
		entry_dict['time'] = ('',self.timestamp.strftime('%H:%M:%S'))
		entry_dict['category'] = ('','USERLOG')
		entry_dict['severity'] = ('','NONE')
		entry_dict['metainfo'] = ('',self.metainfo)
		entry_dict['email'] = ('','')
		entry_dict['location'] = ('','not_set')
		entry_dict['backlink'] = ('','')
		
		if self.file_path:
			(file_type, file_encoding) = mimetypes.guess_type(self.file_path)
			(path, filename) = os.path.split(self.file_path)
			entry_dict['image'] = (filename, open(self.file_path, 'rb'), file_type)
			
		return entry_dict
	
	def creation_url(self, logname, timestamp):
		year = timestamp.strftime('%Y')
		week = str(int(timestamp.strftime('%W'))+1).zfill(2)
		month = timestamp.strftime('%m')
		day = timestamp.strftime('%d')
		base_url = "http://physics-elog.slac.stanford.edu/elog/FileEdit?file=/{0}/data/{1}/{2}/{3}.{4}&xsl=/elogbook/xsl/elog-fileform.xsl&mode=create"
		return base_url.format(logname,year,week,day,month)
		
	def submission_url(self, logname, timestamp):
		r = requests.get(self.creation_url(logname, timestamp))
		self.response = r
		r.raise_for_status()
		m = re.search('action="(.*?)"',r.text)
		if m:
			return m.group(1)
		else:
			return None
				
	
	def submit(self, logname):
		if self.timestamp == None:
			self.timestamp = datetime.now()
		
		submit_url = self.submission_url(logname, self.timestamp)
		if submit_url == None:
			return False
		
		xml_filename = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}-[0-9]{2}\.xml',submit_url).group(0)
		self.metainfo = xml_filename
		r = requests.post(submit_url, files=self.to_dict())
		self.response = r
		r.raise_for_status()
		entry_url = "http://physics-elog.slac.stanford.edu/{0}/show.jsp?dir=/{1}/{2}/{3}.{4}&pos={5}"
		week = str(int(self.timestamp.strftime('%W'))+1).zfill(2)
		return entry_url.format(logname, self.timestamp.strftime('%Y'), week, self.timestamp.strftime('%d'), self.timestamp.strftime('%m'), self.timestamp.strftime('%Y-%m-%dT%H:%M:%S'))
		