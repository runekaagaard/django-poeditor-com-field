=====
Usage
=====

To use Django poeditor.com Model Field in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'poeditor_com_field.apps.PoeditorComFieldConfig',
        ...
    )

Add Django poeditor.com Model Field's URL patterns:

.. code-block:: python

    from poeditor_com_field import urls as poeditor_com_field_urls


    urlpatterns = [
        ...
        url(r'^', include(poeditor_com_field_urls)),
        ...
    ]
