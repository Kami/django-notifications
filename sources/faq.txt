==========================
Frequently asked questions
==========================

Frequently asked questions and answers.

Why are messages not tied / connected to a specific model?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Message templates are not tied to a specific model, because this allows you to have "common" templates which can be used for notifications on different models.

Keep in mind thought, that in the template tags you are only allowed to use fields which are common to all the models which use that template.

Lets say you have two models, one named ``Post`` (``title``, ``date_added``, ``content``, ``author``) and other named ``Links`` (``title``, ``date_added``, ``url``, ``visits``).

In this case, your message template could only refer to the title (``{{ title }}``) and the date_added (``{{ date_added }}``) fields.

