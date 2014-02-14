Welcome to Host the Docs
===========

Host the Docs is a simple way to host static code documentation. Its main use is as a self-hosted server for your organization's private documentation. Better alternatives are available for open source projects, such as Read the Docs or Github Pages.

Host the Docs was created after a long day of banging my head against the wall trying to get Read the Docs set up with private GitHub repositories, and having developed a plugin to get it to work with Perforce. What the world needed was a way to easily host documentation from several projects, from any source, that could build documentation on an individual basis.

Seriously, let other people generate their own docs, I just want to Host the Docs!

Using Host the Docs
====

It's really easy. There's an endpoint for uploading your documentation as a zip file, along with some metadata which controls how your project is displayed on the Host the Docs index. First, run ``runserver.py`` with your preferred WSGI server. We'll use the gevent WSGI server, because it's easy, and we just want to host the damn docs.::

    $ python runserver.py
    
Now, you just need to upload your documentation to the ``/htfd`` URL.
