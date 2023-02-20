=====
Usage
=====

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
