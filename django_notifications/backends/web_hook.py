import urllib

from __init__ import get_settings
from base import BaseBackend


# Backend default settings and meta data
SETTINGS = {
	'meta': {
		'NAME': 'WebHook backend',
		'DESCRIPTION': 'Backend which sends POST data to the specified URL',
		'MESSAGE_REQUIRED': False,
	},
	
	'required': {
		'PAYLOAD_FIELD_NAME': 'payload',
	},
	
	'optional': {
	}
}

class WebHookBackend(BaseBackend):
	def __init__(self):
		self.meta		= SETTINGS['meta']
		self.settings	= get_settings('web_hook')
	
	def is_configured(self):
		return super(WebHookBackend, self).is_configured(self.settings, \
													SETTINGS['required'].keys())
		
	def send(self, url, data):
		if isinstance(data, dict):
			data = self.__format_data(data)
			post_data = {self.settings['PAYLOAD_FIELD_NAME']: data}
			post_data = urllib.urlencode(post_data)
		else:
			post_data = data
		
		request = urllib.urlopen(url, post_data)
	
	def __format_data(self, data):
		
		data_formatted = {}
		for key, value in data.items():
			data_formatted[key] = str(value)
			
		return data_formatted