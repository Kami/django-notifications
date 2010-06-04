from __init__ import get_settings
from base import BaseBackend

from django.core.mail import send_mail


# Backend default settings and meta data
SETTINGS = {
	'meta': {
		'NAME': 'Email backend',
		'DESCRIPTION': 'Backend which sends email notifications',
	},
	
	'required': {
		'SUBJECT': 'No subject',
		'SENDER_EMAIL': '',
	},
	
	'optional': {
	}
}

class EmailBackend(BaseBackend):
	def __init__(self):
		self.meta		= SETTINGS['meta']
		self.settings	= get_settings('email')
	
	def is_configured(self):
		return super(EmailBackend, self).is_configured(self.settings, \
													SETTINGS['required'].keys())
		
	def send(self, email_address, message):
		message = message.encode('utf-8')
		send_mail(self.settings['SUBJECT'], message, \
				self.settings['SENDER_EMAIL'], [email_address])