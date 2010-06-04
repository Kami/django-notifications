from __init__ import get_settings
from base import BaseBackend

try:
	from ..postmark import PMMail
except ImportError:
	not_available = True


# Backend default settings and meta data
SETTINGS = {
	'meta': {
		'NAME': 'Postmark Email backend',
		'DESCRIPTION': 'Backend which is using postmarkapp.com service to send emai notifications',
	},
	
	'required': {
		'API_KEY': '',
		'SUBJECT': 'No subject',
		'SENDER_EMAIL': '',
	},
	
	'optional': {
	}
}

class PostmarkBackend(BaseBackend):
	def __init__(self):
		self.meta		= SETTINGS['meta']
		self.settings	= get_settings('postmark')
	
	def is_configured(self):
		return super(PostmarkBackend, self).is_configured(self.settings, \
													SETTINGS['required'].keys())
		
	def send(self, email_address, message):
		message = message.encode('utf-8')

		# A bit "hacky", but we are not using the Django email backend provided
		# by the Postmark library and we want to skip Django settings import done
		# by the module
		import sys
		django_module = sys.modules['django']
		sys.modules['django'] = None
		
		mail = PMMail(api_key = self.settings['API_KEY'], \
						sender = self.settings['SENDER_EMAIL'], \
						to = email_address, subject = self.settings['SUBJECT'], \
						text_body = message)
		mail.send()
		
		sys.modules['django'] = django_module