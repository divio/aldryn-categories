############
Installation
############


*******************
Installing packages
*******************

Then run either::

    pip install aldryn-categories

or to install from the latest source tree::

    pip install -e git+https://github.com/aldryn/aldryn-categories.git#egg=aldryn-categories


***********
settings.py
***********

In your project's ``settings.py`` make sure you have all of::

    'parler',
    'treebeard',
    'aldryn_categories',

listed in ``INSTALLED_APPS``.


****************************
Prepare the database and run
****************************

Now run ``python manage.py migrate`` to prepare the database for the new
application, then ``python manage.py runserver``.


****************
For Aldryn users
****************

On the Aldryn platform, the Addon is available from the `Marketplace
<http://www.aldryn.com/en/marketplace>`_.

You can also `install Aldryn Categories into any existing Aldryn project
<https://control.aldryn.com/control/?select_project_for_addon=aldryn-categories>`_.
