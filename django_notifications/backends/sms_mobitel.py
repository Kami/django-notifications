from __init__ import get_settings
from base import BaseBackend

try:
	from suds.client import Client
except ImportError:
	not_available = True


# Default settings
SETTINGS = {
	'meta': {
		'NAME': 'Mobitel.si SMS backend',
		'DESCRIPTION': 'Backends which sends SMS notifications using mobitel.si SOAP API',
		'WS_URL': 'https://moj.mobitel.si/mobidesktop-v1/wsdl.xml',
	},
	
	'required': {
		'USERNAME': '',
		'PASSWORD': '',
	},
	
	'optional': {
	}
}

class SMSMobitelBackend(BaseBackend):
	def __init__(self):
		self.meta				= SETTINGS['meta']
		self.settings			= get_settings('sms_mobitel')
	
	def is_configured(self):
		return super(SMSMobitelBackend, self).is_configured(self.settings, \
													SETTINGS['required'].keys())
		
	def send(self, phone_number, message):
		messages = self.__format_message(message)
		
		for message in messages:
			self.__send_sms(phone_number, message)
	
	def __send_sms(self, phone_number, message):
		client = Client(self.meta['WS_URL'])
		recipients = client.factory.create('ArrayOfString')
		recipients.string = phone_number
		client.service.SendSMS(self.settings['USERNAME'], self.settings['PASSWORD'], \
								recipients, message)
		
	def __format_message(self, message):
		"""
		Splits a single message into multiple ones, if the text is longer then
		160 characters.
		"""
		messages = []
		message_len = len(message)
		if message_len > 160:
			curr_pos = 0
			chars_left = message_len - 160
			
			while chars_left > 0:
				message_new = message[curr_pos : curr_pos + 160]
				message_new_len = len(message_new)
				chars_left -= message_new_len
				curr_pos += message_new_len
				
				messages.append(message_new)
		else:
			messages = [message]
				
		return messages