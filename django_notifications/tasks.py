from django.template.loader import render_to_string
from django.template import Template, Context

from celery.task import Task
from celery.registry import tasks

from models import MODEL_ACTIONS, NOTIFICATION_TYPES
from models import SubscriptionMap, Message
from models import get_choice_id

from backends import get_class_instance_by_key
from django.db.models import Q

class NotificationTask(Task):
	ignore_result = True
	
	def run(self, type, subscriber, message):
		# Before disptaching the notification we check if this backend
		# is actually configured and available.
		if not get_choice_id(type, NOTIFICATION_TYPES, reverse = True):
			return
		
		notification_class = get_class_instance_by_key(type)
		notification_class.send(subscriber, message)
	
class CheckSubscriptionsTask(Task):
	ignore_result = True
	
	def run(self, model, object_id, action, field_values):
		subscriptions = SubscriptionMap.objects.filter(
										subscription__model_content_type__model = model, \
										subscription__action = action, \
										subscription__active = True, active = True)
		
		for subscription in subscriptions:
			# Dispatch the notification tasks
			model_object_id = subscription.subscription.model_object_id
			
			if model_object_id and (model_object_id != object_id):
				# Subscribed for an event on a single object, but the
				# object ID doesnt match.
				continue
			
			type = subscription.type
			subscriber = subscription.recipient
			message = subscription.message.content
			template = Template(message)
			
			field_values.update({'model': model,
								'action': get_choice_id(action, MODEL_ACTIONS, \
														 reverse = True)})
			context = Context(field_values)
			message_rendered = template.render(context)
			
			NotificationTask.delay(type, subscriber, message_rendered)
			
			if model_object_id and (action == get_choice_id('delete', MODEL_ACTIONS)):
				# Subscribed for delete event on a single object.
				# Subscription is de-activated after the notification task has been
				# dispatched.
				subscription.subscription.active = False
				subscription.subscription.save()