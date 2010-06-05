from django.db import models

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from django.contrib.contenttypes import generic
from django.db.models.signals import post_save, post_delete

from backends import get_available_backends

# Constans
MODEL_ACTIONS = (
	(0, 'create'),
	(1, 'edit'),
	(2, 'delete')
)

configured_backends = [(backend[0], backend[1]) for backend in \
					get_available_backends(configured_only = True)]
NOTIFICATION_TYPES = configured_backends

# Models
class Message(models.Model):
	"""
	The message which is dispatched using the selected backend.
	
	Each message is rendered as a Django template and provided with
	all the instance attributes from the model which has triggered this signal
	including the model and action name.
	
	Lets say you have a model News with the following fields:
	
	- id
	- title
	- author
	- date_submitted
	- content
	
	Your message could then look like this:
	
	User {{ author.username }} has added a new news with the title {{ title }} 
	to the website today at {{ date_subbmited|format:"d.m.Y" }}.
	"""
	label = models.CharField(max_length = 150)
	content = models.TextField(blank = False)
	
	def __unicode__(self):
		return '%s' % (self.label)
	
class Subscription(models.Model):
	"""
	Subscriptions.
	"""
	label = models.CharField(max_length = 150)
	user = models.ForeignKey(User, blank = True, null = True)
	model_content_type = models.ForeignKey(ContentType, verbose_name = 'model', \
											db_index = True)
	model_object_id = models.PositiveIntegerField(blank = True, null = True)
	action = models.PositiveIntegerField(max_length = 1, choices = MODEL_ACTIONS,
											db_index = True)
	date_subscribed = models.DateTimeField(auto_now_add = True)
	active = models.BooleanField(default = True)
	
	def clean(self):
		from django.core.exceptions import ValidationError
		
		if self.model_object_id:
			# If the model object ID is specified, check that the instance with
			# this ID actually exists.
			try:
				object = self.model_content_type.get_object_for_this_type(pk = \
																	self.model_object_id)
			except ObjectDoesNotExist:
				raise ValidationError('Model instance with this ID does not exist')
			
			if self.action == get_choice_id('create', MODEL_ACTIONS):
				raise ValidationError('Model object ID must be empty when subscribing for a create event')
			
	def __unicode__(self):
		return '%s' % (self.label)
				
class SubscriptionMap(models.Model):
	"""
	Mapping between subscriptions, notification types and messages.
	"""
	subscription = models.ForeignKey(Subscription)
	message = models.ForeignKey(Message)
	type = models.CharField(max_length = 50, choices = NOTIFICATION_TYPES)
	recipient = models.CharField(max_length = 250) # Email / XMPP address / Mobile phone number
	active = models.BooleanField(default = True)
	
	class Meta:
		verbose_name 		= 'Notification'
		verbose_name_plural = 'Notifications'
		
	def __unicode__(self):
		return '%s - %s (%s)' % (self.subscription, self.type, \
								'enabled' if self.active else 'disabled')

# Signal callbacks
def post_save_callback(sender, **kwargs):
	# Dispatches a task which checks if there are any active subscriptions for this event.
	#
	# Tasks are used, because signals in Django are synchronous (blocking) and if there were
	# many subscribers for this event, this callback could slow things down considerably.
	model = get_model_name(sender.__doc__)
	instance = kwargs['instance']
	created = kwargs['created']
	
	action = get_choice_id('create' if created else 'edit', MODEL_ACTIONS)
	object_id = instance.id
	field_values = get_field_values(instance)
	
	from tasks import CheckSubscriptionsTask
	CheckSubscriptionsTask.delay(model, object_id, action, field_values)
	
def post_delete_callback(sender, **kwargs):
	model = get_model_name(sender.__doc__)
	instance = kwargs['instance']
	
	action = get_choice_id('delete', MODEL_ACTIONS)
	object_id = instance.id
	field_values = get_field_values(instance)
	
	from tasks import CheckSubscriptionsTask
	CheckSubscriptionsTask.delay(model, object_id, action, field_values)
	
# "Helper" methods
def get_model_name(doc_string):
	model_name = doc_string[:doc_string.find('(')].lower()
	
	return model_name
	
def get_field_values(instance):
	field_values = dict([(key, value) for key, value in instance.__dict__.iteritems() \
							if not key.startswith('_')])
	
	return field_values

def get_choice_id(key, values, reverse = False):
	try:
		if not reverse:
			id = [tuple[0] for tuple in values if tuple[1] == key][0]
		else:
			id = [tuple[1] for tuple in values if tuple[0] == key][0]
	except KeyError:
		return None
	
	return id

# Register the callbacks
post_save.connect(post_save_callback)
post_delete.connect(post_delete_callback)