=====
Usage
=====

To use gm-auth-sdk in a project, add it to your `INSTALLED_APPS`:

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
