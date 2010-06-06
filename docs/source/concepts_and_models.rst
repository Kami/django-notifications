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
-------------

This is the main model which creates a mapping between a model event and one or more notifications.

**Fields:**

- ``Label`` - short label for your subscription
- ``User`` - user which this subscription is connected to (can be empty)
- ``Model`` - the model which triggers the event
- ``Model object id`` - ID of the model object which you want to create subscription for (in case you leave this field empty, you subscribe to event for all the model objects)
- ``Model match filter`` - a special match filter (for more information, see :ref:`concepts_and_models-match_filters`)
- ``Action`` - model action which triggers the event (can be ``create``, ``edit`` or ``delete``)
- ``Active`` - you can optionally (temporary) de-active the subscription

Notifications
-------------

Subscription would be useless without a notification so you should create at least one (and possibly more) notifications for your subscription.

**Fields:**

- ``Message`` - refers to the message template which is dispatched using the selected notification backend
- ``Type`` - notification type, for example: Email, Jabber, SMS, .... (this field will only display backends which have been configured properly)
- ``Recipient`` - the recipient of the notification (e.g. email address when using the Email backend, mobile phone number when using the SMS backend, Jabber ID when using the XMPP backend and so on)
- ``Active`` - you can optionally (temporary) de-active the notification

Messages
--------

A message template which is dispatched using the selected notification backend.

**Fields:**

- ``label`` - short label for your message template
- ``content`` - the content of your message

When rendered, each message template is automatically provided with the name of the action and the model which has triggered the event, and also all the model instance field values.

This allows you to use the `Django template tags and filters`_ in the content field of the message templates.

For example, one of your message templates could look like this::

  Profile of the user {{ user.username }} has been updated on {{ date_updated|date:"d.m.Y" }} (model {{ model }}, action {{ action }})

In this case, the model which has triggered this event would need to have at least two fields - ``user`` and ``date_updated``.

.. _concepts_and_models-match_filters:

Model match filters
~~~~~~~~~~~~~~~~~~~

Matching an event based on the model instance field value(s) is currently very limited and simple, but nonetheless you can still use basic ``startswith``, ``endswith`` and ``contains`` filters.

- ``startswith`` filter: <field name>=<field_value>* (e.g. ``title=Just released*``)
- ``endswith`` filter: <field name>=*<field value> (e.g. ``author=*Smith``)
- ``contains`` filter: <field name>=*<field value>* (e.g. ``description=*Saturday morning*``)

You can combine multiple filters using a comma (``,``) - currently only ``AND`` filters are supported.

For example:

- ``title=*Apache*,enabled=True`` - this would match a defined model instance which ``title`` field contains a string ``Apache`` **AND** the ``enabled`` field has a value of ``True``.
- ``status=sent,author=Tomaz,content=*committed*`` - this would match a defined model instance which ``status`` field has a value of ``sent`` **AND** the ``author`` field has a value of ``Tomaz`` **AND**  the ``content`` field contains a string ``committed``.

.. _Django template tags and filters: http://docs.djangoproject.com/en/dev/ref/templates/builtins/
