=============================
Grandmercado Authentication SDK
=============================

.. image:: https://badge.fury.io/py/gm-auth-sdk.svg
    :target: https://badge.fury.io/py/gm-auth-sdk

.. image:: https://travis-ci.org/dfg-98/gm-auth-sdk.svg?branch=master
    :target: https://travis-ci.org/dfg-98/gm-auth-sdk

.. image:: https://codecov.io/gh/dfg-98/gm-auth-sdk/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dfg-98/gm-auth-sdk

Software Development Kit for Grandmercado Authentication.

This package is intended to use only withing Grandmercado ecosystem.
It share common authentication feautes needed for Grandmercado's services.


Quickstart
----------

Install gm-auth-sdk::

    pip install git+https://github.com/Aeroenvio/gm-auth-sdk

Add `GMAuthentication` to `REST_FRAMEWORK`'s `DEFAULT_AUTHENTICATION_CLASSESS`':

.. code-block:: python

    # Django Rest Framework
    REST_FRAMEWORK = {
        ...
        "DEFAULT_AUTHENTICATION_CLASSES": (
            ...
            "gm_auth_sdk.authentication.GMAuthentication",
        ),
    }

Ensure `SIGNING_KEY` in `SIMPLE_JWT` is the same as the authentication service.

On Authentication the user in request will be a
`TokenUser` object. No database lookup will be performed.


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
