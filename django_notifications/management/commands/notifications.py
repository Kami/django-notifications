"""
Django notifications management commands.

Usage:

	python manage.py notifications backends - displays all the available notification
	backends
   
	python manage.py notifications configured_backends - displays all the configured
	notification backends
	
	python manage.py notifications settings [backend_key] - displays the settings for
	the specified backend
"""

from django.core.management.base import BaseCommand, CommandError

from django_notifications import backends
from django_notifications.management.commands.color import style

VALID_COMMANDS = {
	'backends': (0, None),
	'configured_backends': (0, None),
	'settings': (1, '[backend name]')
}


class Command(BaseCommand):
	help = 'Manage notifications'
	args = 'subcommand'
	requires_model_validation = False

	def handle(self, *args, **kwargs):		
		if len(args) == 0:
			raise CommandError('You need to specify a subcommand: %s' % \
							(', ' . join(VALID_COMMANDS)))
		else:
			sub_command = args[0]
			
			if not sub_command in VALID_COMMANDS.keys():
				raise CommandError('Invalid subcommand specified. Valid choices are: %s' % \
							(', ' . join(VALID_COMMANDS.keys())))
			
			argument_count = VALID_COMMANDS[sub_command][0]
			argument_help = VALID_COMMANDS[sub_command][1]
			
			if argument_count != len(args) - 1:
				raise CommandError('Invalid number of arguments. Usage: %s %s' % \
							(sub_command, argument_help if argument_help else ''))
				
			command = getattr(self, 'CMD_%s' % (sub_command))
			command(*args[1:])
			
	def CMD_backends(self):
		try:
			available_backends = backends.get_available_backends()

			print style.GREEN('Available backends:')
			for (key, value, description) in available_backends:
				print '- ', style.BOLD('%s' % (key)), '- %s (%s)' % (value, description)
		except KeyboardInterrupt:
			pass
				
	def CMD_configured_backends(self):
		try:
			configured_backends = backends.get_available_backends(configured_only = True)
			
			print style.GREEN('Available and configured backends:')
			for (key, value, description) in configured_backends:
				print '- ', style.BOLD('%s' % (key)), '- %s (%s)' % (value, description)
		except KeyboardInterrupt:
			pass
		
	def CMD_settings(self, backend_key):
		try:
			backend_settings = backends.get_settings(backend_key)

			print style.GREEN('Settings for "%s" backend:' % (backend_key))
			for (key, value) in backend_settings.iteritems():
				print style.BOLD('%s:' % (key)), '\t\t %s' % (value)
		except EnvironmentError:
			print 'Invalid backend key'
		except KeyboardInterrupt:
			pass