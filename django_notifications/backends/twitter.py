from __init__ import get_settings
from base import BaseBackend

try:
	from ..twitter import *
except ImportError:
	not_available = True


# Default settings
SETTINGS = {
	'meta': {
		'NAME': 'Twitter Backend',
		'DESCRIPTION': 'Backend which sends notifications to Twitter',
		'MESSAGE_REQUIRED': True,
	},
	
	'required': {
		'USERNAME': '',
		'PASSWORD': '',
	},
	
	'optional': {
	}
}

class TwitterBackend(BaseBackend):
	def __init__(self):
		self.meta		= SETTINGS['meta']
		self.settings	= get_settings('twitter')

	def is_configured(self):
		return super(TwitterBackend, self).is_configured(self.settings, \
													SETTINGS['required'].keys())
		
	def send(self, recipient, message):
		# Truncate the message down if it's too long
		message = '%s...' % (message[:120]) if len(message) >= 120 else message
		twitter_api = Api(self.settings['USERNAME'], self.settings['PASSWORD'])
		
		try:
			if recipient.startswith('@'):
				# If username is specified, send a direct message to this user, else
				# discard the recipient and just send a regular status update
				recipient = recipient[1:]
				twitter_api.PostDirectMessage(recipient, message.encode('utf-8'))
			else:
				twitter_api.PostUpdate(status = message.encode('utf-8'))
		except HTTPError:
			pass