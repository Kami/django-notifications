from __init__ import get_settings
from base import BaseBackend

import time

try:
	from ..xmpp import *
except ImportError:
	not_available = True


# Default settings
SETTINGS = {
	'meta': {
		'NAME': 'XMPP Backend',
		'DESCRIPTION': 'Backend which sends notifications using XMPP (Jabber) protocol',
	},
	
	'required': {
		'JID': '',
		'PASSWORD': '',
		'SERVER': 'talk.google.com',
		'PORT': 5222,
	},
	
	'optional': {
	}
}

class XMPPBackend(BaseBackend):
	def __init__(self):
		self.meta		= SETTINGS['meta']
		self.settings	= get_settings('xmpp')

	def is_configured(self):
		return super(XMPPBackend, self).is_configured(self.settings, \
													SETTINGS['required'].keys())
		
	def send(self, recipient_jid, message):
		client = self.__authenticate_and_get_client()
		
		if not client:
			return None
		
		client.send(protocol.Message(recipient_jid, message))
		
		time.sleep(1)
		client.disconnect()
		
	def __authenticate_and_get_client(self):
		jid = protocol.JID(self.settings['JID'])
		client = Client(jid.getDomain(), debug = [])
		connection = client.connect(server = (self.settings['SERVER'], \
									self.settings['PORT']))
		
		if not connection:
			return None
		
		auth = client.auth(jid.getNode(), self.settings['PASSWORD'], \
						  resource = jid.getResource())
		
		if not auth:
			return None
		
		return client