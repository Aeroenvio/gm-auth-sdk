=============================
gm-auth-sdk
=============================

.. image:: https://badge.fury.io/py/gm-auth-sdk.svg
    :target: https://badge.fury.io/py/gm-auth-sdk

.. image:: https://travis-ci.org/dfg-98/gm-auth-sdk.svg?branch=master
    :target: https://travis-ci.org/dfg-98/gm-auth-sdk

.. image:: https://codecov.io/gh/dfg-98/gm-auth-sdk/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dfg-98/gm-auth-sdk

SDK for Grandmercado Authentication

Documentation
-------------

The full documentation is at https://gm-auth-sdk.readthedocs.io.

Quickstart
----------

Install gm-auth-sdk::

    pip install gm-auth-sdk

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'gm_auth_sdk.apps.GmAuthSdkConfig',
        ...
    )

Add gm-auth-sdk's URL patterns:

.. code-block:: python

    from gm_auth_sdk import urls as gm_auth_sdk_urls


    urlpatterns = [
        ...
        url(r'^', include(gm_auth_sdk_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
