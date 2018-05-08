====================
django-codenerix-cms
====================

Codenerix CMS is a module that enables `CODENERIX.com <http://www.codenerix.com/>`_ to set products on several platforms in a general manner

.. image:: http://www.codenerix.com/wp-content/uploads/2018/05/codenerix.png
    :target: http://www.codenerix.com
    :alt: Try our demo with Codenerix Cloud

****
Demo
****

Coming soon...

**********
Quickstart
**********

1. Install this package::

    For python 2: sudo pip2 install django-codenerix-cms
    For python 3: sudo pip3 install django-codenerix-cms

2. Add "codenerix_extensions" and "codenerix_cms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'codenerix_extensions',
        'codenerix_cms',
    ]

3. For use StaticPage, you must create a bridge inheriting from GenStaticPage, and implementing the methods::

    * CDNXCMS_get_fk_info_author: return a dictionary with the keys 'label' and 'related'.
        - label: label translated for the input
        - related: it is a string with related_name for genforeignkey
    * CDNXCMS_get_name_related: return a string with the name of the model's field that contains the name of the author

4. Since Codenerix CMS is a library, you only need to import its parts into your project and use them.

*************
Documentation
*************

Coming soon... do you help us? `Codenerix <http://www.codenerix.com/>`_

*******
Credits
*******

This project has been possible thanks to `Centrologic <http://www.centrologic.com/>`_.
