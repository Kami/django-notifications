===============================
Available notification backends
===============================

Here is the list of the available notification backends.

You configure your backend(s) by putting the appropriate settings in your project settings file (this will most likely be ``settings.py``).

email
~~~~~

This backend uses Django e-mail wrapper for sending e-mail notifications.

**Dependencies**:

- None

**Settings**:

- ``SUBJECT`` - the subject of your email
- ``SENDER_EMAIL`` - email address of the sender

For example::

	NOTIFICATIONS = {
		'email': {
			'SUBJECT': 'Your subject',
			'SENDER_EMAIL': 'name@domain.com',
		},
	}
	

xmpp
~~~~

This backend uses XMPP protocol for sending the notifications.

**Dependencies**:

- xmpppy library (http://xmpppy.sourceforge.net)

**Settings**:

- ``JID`` - your Jabber ID (username)
- ``PASSWORD`` - your password
- ``SERVER`` - XMPP server (default = talk.google.com)
- ``PORT`` - server port (default = 5222)

For example::

	NOTIFICATIONS = {
			'xmpp': {
				'JID': 'me@mydomain.com',
				'PASSWORD': 'HsdeoUns18AT18E',
		},
	}
	
Note that we didn't specify the ``SERVER`` and the ``PORT`` setting, meaning that the default values will be used.

sms_mobitel
~~~~~~~~~~~

**Dependencies**:

- SUDS library (https://fedorahosted.org/suds/)

This backend uses `Mobitel.si` service to send SMS messages (only available to Mobitel.si subscribers in Slovenia)

**Settings**:

- ``USERNAME`` - your phone number
- ``PASSWORD`` - your password

For example::

	NOTIFICATIONS = {
			'sms_mobitel': {
				'USERNAME': '031123456',
				'PASSWORD': 'somepassword12',
		},
	}

postmark
~~~~~~~~

This backend uses http://postmarkapp.com REST service to send email.

**Dependencies**:

- PostmarkApp library (http://github.com/themartorana/python-postmark)

**Settings**:

- ``API_KEY`` - your PostmarkApp API key
- ``SUBJECT`` - the subject of your email
- ``SENDER_EMAIL`` - email address of the sender

For example::

	NOTIFICATIONS = {
		'postmark': {
			'API_KEY': 'f8469hg8as1-5g87sdf9sde03-41ae86',
			'SUBJECT': 'Your subject',
			'SENDER_EMAIL': 'name@domain.com',
		},
	}
	
twitter
~~~~~~~

This backends sends notifications to Twitter_.

When you set a recipient in the admin panel, you can specify a Twitter account username (``@Username``) and the backend will send this user a `direct message`_.

If anything else not starting with an at sign is specified, the ``recipient`` field is ignored and a normal `status update`_ is posted.

**Dependencies**:

- python-twitter library (http://code.google.com/p/python-twitter/)

**Settings**:

- ``USERNAME`` - your Twitter account username
- ``PASSWORD`` - your Twitter account password

For example::

	NOTIFICATIONS = {
			'twitter': {
				'USERNAME': 'Tweetie',
				'PASSWORD': 'somepassword1298',
		},
	}
	
*Note: If you want to send a direct message, the user which you want to send the message to must follow you and vice-versa.*

.. _Mobitel.si: https://moj.mobitel.si/portal
.. _Twitter: http://twitter.com/
.. _direct message: http://help.twitter.com/forums/10711/entries/14606
.. _status update: http://help.twitter.com/entries/15367-how-to-post-a-twitter-update-or-tweet
