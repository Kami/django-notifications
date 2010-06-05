# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import re
from distutils.core import setup

version_re = re.compile(
    r'__version__ = (\(.*?\))')

cwd = os.path.dirname(os.path.abspath(__file__))
fp = open(os.path.join(cwd, 'django_notifications', '__init__.py'))

version = None
for line in fp:
    match = version_re.search(line)
    if match:
        version = eval(match.group(1))
        break
else:
    raise Exception('Cannot find version in __init__.py')
fp.close()

setup(name = 'django_notifications',
	  version = '.' . join(map(str, version)),
	  description = 'Django application which allows you to make subscriptions for different model events (create, edit and delete) and send notification(s) when the subscribed event has occurred.',
	  author = 'Tomaž Muraus',
	  author_email = 'kami@k5-storitve.net',
	  license = 'GPL',
	  url = 'http://kami.github.com/django-notifications/',
	  download_url = 'http://github.com/Kami/django-notifications/downloads/',
	  packages = ['django_notifications', 'django_notifications.backends', \
				 'django_notifications.management', 'django_notifications.management.commands'],
	  requires = ['django(>=1.2)', 'celery'],
	  provides = ['django_notifications'],
	  
	  classifiers = [
		  'Development Status :: 3 - Alpha',
		  'Environment :: Web Environment',
		  'Framework :: Django',
		  'Intended Audience :: Developers',
		  'License :: OSI Approved :: GNU General Public License (GPL)',
		  'Operating System :: OS Independent',
		  'Programming Language :: Python',
		  'Topic :: Internet :: WWW/HTTP',
		  'Topic :: Software Development :: Libraries',
	],
)