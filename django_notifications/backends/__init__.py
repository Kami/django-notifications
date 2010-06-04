import sys

from django.conf import settings


BACKEND_CLASSES = {
	'email': 'django_notifications.backends.email.EmailBackend',
	'xmpp': 'django_notifications.backends.xmpp.XMPPBackend',
	'sms_mobitel': 'django_notifications.backends.sms_mobitel.SMSMobitelBackend',
	'postmark': 'django_notifications.backends.postmark.PostmarkBackend',
}

def get_available_backends(configured_only = False):
	"""
	Returns a list of all the available backends.
	
	If configured_only = True only those backends which are
	properly configured are returned.
	"""
	available_backends = []
	for key in BACKEND_CLASSES.keys():
		module_name = get_module_and_class_name(BACKEND_CLASSES[key])[0]
		class_instance = get_class_instance_by_key(key)
		module = sys.modules[module_name]
		
		try:
			not_available = getattr(module, 'not_available')
		except AttributeError:
			not_available = None
		
		is_configured = getattr(class_instance, 'is_configured', False)()
		meta = getattr(class_instance, 'meta', None)
		
		if not meta or (configured_only and not is_configured) \
					or (configured_only and not_available):
			continue
			
		name = meta['NAME']
		description = meta['DESCRIPTION']

		available_backends.append((key, name, description))
			
	return available_backends

def get_settings(backend_key, use_default = True):
	"""
	Returns all the settings for the provided backend key.
	"""
	notification_settings = getattr(settings, 'NOTIFICATIONS', None)

	if not BACKEND_CLASSES.get(backend_key, None):
		raise EnvironmentError('Invalid backend: %s' % (backend_key))
	
	if not notification_settings:
		raise EnvironmentError('NOTIFICATIONS was not found.')
	
	# Default backend settings
	if use_default:
		module_name = get_module_and_class_name(BACKEND_CLASSES[backend_key])[0]
		__import__(module_name)
		module = sys.modules[module_name]
		backend_settings = getattr(module, 'SETTINGS')['required']
	else:
		backend_settings = {}

	try:
		backend_settings.update(notification_settings[backend_key])
	except KeyError:
		pass
		
	return backend_settings

# "Helper" methods
def get_module_and_class_name(class_path):
	module_name = class_path[:class_path.rfind('.')]
	class_name = class_path[class_path.rfind('.') + 1:]
		
	return module_name, class_name	

def get_class_instance_by_key(key):
	try:
		class_path = BACKEND_CLASSES[key]
	except KeyError:
		return None
	
	module_name, class_name = get_module_and_class_name(class_path)
	__import__(module_name)
	
	module = sys.modules[module_name]
	class_instance = getattr(module, class_name)()
	
	return class_instance