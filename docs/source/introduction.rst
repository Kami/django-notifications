============
Introduction
============

django_notifications is an application which allows you to make subscriptions for different model events (create, edit and delete) and send notification(s) when the event you have created subscription for has occurred.

You can subscribe to an event for all the model objects (current and new ones which will be created) or you can choose to only subscribe to an event for a specific model object.

For example, lets say you are running a social-network website and your application contains a module named ``Profile`` which contains the following fields:

- user
- full_name
- location
- bio
- date_created
- date_updated

You could then create a subscription on the model ``Profile`` for action ``create``.

In this case, the event would be triggered (and notification dispatched) every time a new Profile object is created.

On the other hand, lets say you are only interested when an object with ID 500 is updated / edited.

You can create a subscription on the model ``Profile`` and the ``model object ID`` 500 for an action ``edit``.

Now, the event would only be triggered when a object with ID 500 is edited.

*Note: If you subscribe to a delete event for a specific model object, the subscription is automatically disabled after the event has been triggered and notification dispatched.

The reason is that is makes no sense staying subscribed to this event, since it won't happen anymore, because the object has been deleted.

Available notification backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently this module supports the following notification backends / protocols:

- Email - uses Django e-mail wrapper for sending e-mail
- XMPP - uses XMPP protocol for sending notifications (Google Talk, etc.)
- SMS - uses `Mobitel.si` service to send SMS messages (only available to Mobitel.si subscribers in Slovenia)
- Postmark Email - uses http://postmarkapp.com REST service to send email
- Twitter - sends notifications to Twitter (as a direct message or a normal status update)

For more information, visit the :doc:`available_notification_backends` page.

.. _Mobitel.si: https://moj.mobitel.si/portal
