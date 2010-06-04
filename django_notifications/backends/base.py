class BaseBackend(object):
	
	def is_configured(self, settings, required_keys):
		"""
		Returns True if all the required settings have been configured,
		False otherwise.
		"""
		for key in required_keys:
			if not settings.get(key, None) or \
				not settings.get(key):
				return False
			
		return True
	
	def send(self, recipient, message):
		"""
		This method sends the notification.
		
		recipient - The actual recipient - e.g. for email backend
		this would be the email adress.
		message - The actual rendered message.
		"""
		pass