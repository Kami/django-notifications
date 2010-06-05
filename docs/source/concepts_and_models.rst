====================
Concepts and models
====================

To use this application, you need to understand some basic concepts and models this applications uses.

How does it work?
~~~~~~~~~~~~~~~~~

TODO

Models
~~~~~~~

Subscriptions
--------------

This is the main model which creates a mapping between model event and notifications.

**Fields:**

- ``Label`` - short label for your subscription
- ``User`` - user which this subscription is connected to (can be empty)
- ``Model`` - the model which will trigger the event
- ``Model object id`` - the specific model object which you want to create subscription for (in case you leave this empty, you subscribe to event for all the model objects)
- ``Action`` - model action which will trigger the event (can be create, edit or delete)
- ``Active`` - you can optionally (temporary) de-active the subscription

Notifications
--------------

Subscription would be useless without a notification so you should create at least one (and possibly more) notifications for your subscription.

**Fields:**

- ``Messages`` - refers to the message template which is dispatched using the selected notification backend
- ``Type`` - notification type, for example: Email, Jabber, SMS, .... (this field will only display those backends which have been configured properly)
- ``Recipient`` - the recipient of the notification (e.g. email address when using the Email backends, mobile phone number when using the SMS backend, Jabber ID when using the XMPP backend and so on)
- ``Active`` - you can optionally (temporary) de-active the subscription


Messages
---------

That is the message template which is dispatched using the selected notification backend.

**Fields:**

- ``label`` - short label for your message
- ``content`` - your message content

When rendered, each message template is automatically provided with the name of the action and the model which has triggered the event, and also all the model instance field values.

This allows you to use the Django template tags in the content field of the message templates.

For example, one of your message templates could then look like this::

  Profile of the user {{ user.username }} has been updated on {{ date_updated|date:"d.m.Y" }} (model {{ model }}, action {{ action }})

In this case, the model which has triggered this event would need to have at least two fields - ``user`` and ``date_updated``.