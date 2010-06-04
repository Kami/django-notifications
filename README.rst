Django application which allows you to make subscriptions for different model events (create, edit and delete) and send notification(s) when the event you have created subscription for has occurred.

Currently it supports the following notification backends / protocols:

- Email (using Django wrapper for sending e-mail)
- XMPP
- Postmark Email (using http://postmarkapp.com service)
- SMS (using mobitel.si web service - Slovenian users only)