from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

from models import Subscription, SubscriptionMap, \
				   Message


class SubscriptionMapInline(admin.StackedInline):
	model = SubscriptionMap
	max_num = 5
	
class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ('label', 'model_content_type', 'model_instance', 
					'action', 'date_subscribed', \
					'active', 'notification_count_all', \
					'notification_count_active')
	list_filter = ('model_content_type',)
	date_hierarchy = 'date_subscribed'
	search_fields = ('label', 'subscriptionmap__message__label',)
	
	inlines = [ SubscriptionMapInline ]
	
	def model_instance(self, obj):
		try:
			content_type = ContentType.objects.get(model = obj.model_content_type)
			model_instance = content_type.get_object_for_this_type(pk = \
																obj.model_object_id)
			
			# Not exactly sure, why "obj.model_content_type.get_object_for_this_type()"
			# returns None here
			return str(model_instance)
		
		except ObjectDoesNotExist:
			return str(obj.model_object_id)
	
	def notification_count_all(self, obj):
		return obj.subscriptionmap_set.count()
	notification_count_all.short_description = 'Notification count (all)'
	
	def notification_count_active(self, obj):
		return obj.subscriptionmap_set.filter(active = True).count()
	notification_count_active.short_description = 'Notification count (active)'

class SubscriptionMapAdmin(admin.ModelAdmin):
	list_display = ('subscription', 'message', 'type', 
					'recipient', 'active')
	search_fields = ('subscription__label',)

class MessageAdmin(admin.ModelAdmin):
	model = Message
	
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionMap, SubscriptionMapAdmin)
admin.site.register(Message, MessageAdmin)