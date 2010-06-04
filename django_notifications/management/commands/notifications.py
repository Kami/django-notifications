"""
Django notifications management commands.

Usage:

	python manage.py notifications backends - displays all the available notification
	backends
   
	python manage.py notifications configured_backends - displays all the configured
	notification backends
	
	python manage.py notifications settings [backend_key] - displays the settings for
	the specified backend.
"""

from django.core.management.base import BaseCommand, CommandError

from django_notifications import backends


class Command(BaseCommand):
	help = 'Manage notifications'
	args = 'subcommand'
	requires_model_validation = False
	
	def handle(self, *args, **kwargs):
		valid_commands = ('backends', 'configured_backends', 'settings')
		
		if len(args) == 0:
			raise CommandError('You need to specify a subcommand: %s' % \
							(', ' . join(valid_commands)))
		elif len(args) > 1 and args[0] != 'settings':
			raise CommandError('Invalid number of arguments: %s' % \
							(', ' . join(args)))
		else:
			sub_command = args[0]
			
			if not sub_command in valid_commands:
				raise CommandError('Invalid subcommand specified. Valid choices are: %s' % \
							(', ' . join(valid_commands)))
				
			if sub_command == 'settings' and len(args) != 2:
				raise CommandError('Invalid number of arguments. Usage %s [backend_key]' % \
							(', ' . join(args)))
				
			command = getattr(self, 'CMD_%s' % (sub_command))
			command(*args[1:])
			
	def CMD_backends(self):
		try:
			available_backends = backends.get_available_backends()
			
			print 'Available backends:'
			for (key, value, description) in available_backends:
				print '%s - %s (%s)' % (key, value, description)
		except KeyboardInterrupt:
			pass
				
	def CMD_configured_backends(self):
		try:
			configured_backends = backends.get_available_backends(configured_only = True)
			
			print 'Available and configured backends:'
			for (key, value, _) in configured_backends:
				print '%s - %s' % (key, value)
		except KeyboardInterrupt:
			pass
		
	def CMD_settings(self, backend_key):
		try:
			backend_settings = backends.get_settings(backend_key)

			print '%s backend settings:' % (backend_key)
			for (key, value) in backend_settings.iteritems():
				print '%s:\t\t %s' % (key, value)
		except EnvironmentError:
			print 'Invalid backend key'
		except KeyboardInterrupt:
			pass