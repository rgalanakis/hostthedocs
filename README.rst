Welcome to Host the Docs
========================

Host the Docs is a simple way to host static code documentation. Its main use is as a self-hosted server for your organization's private documentation. Better alternatives are available for open source projects, such as Read the Docs or Github Pages.

Host the Docs was created after a long day of banging my head against the wall trying to get Read the Docs set up with private GitHub repositories, and having developed a plugin to get it to work with Perforce. What the world needed was a way to easily host documentation from several projects, from any source, that could build documentation on an individual basis.

Seriously, let other people generate their own docs, I just want to Host the Docs!

Running the server
------------------

Host the Docs is built with Flask, so it should be easy enough to set up and run, even if you aren't a competent web programmer. You don't even have to run Host the Docs with Apache or whatever WSGI server of your choice, even though I recommend it. Run the first command to use a gevent webserver, and the second to use the builtin Flask reloading server.
::

    $ python runserver.py
    $ python runserver.py --config DEV
    
Under the hood, the server uses a SQLlite DB to cache information, like what docs are available. There's no DB server to run or configure. Host the Docs just uses files for pretty much everything.

Generating your docs
--------------------

Figure it out yourself! Host the Docs uses Sphinx to generate its html documentation, then zips up the ``build/html`` folder and sends it to a Host the Docs server. See ``create_the_docs.py``.

Uploading your docs
-------------------

There's a single URL endpoint, ``/hmfd`` (easy to remember: "host my fucking docs"). You give it a JSON document containing some simple metadata::

    {
      "name": "Host the Docs",
      "version": "0.1.0",
      "description": "Host the Docs makes hosting any HTML documentation simple."
    }
    
And a ``.zip`` file that has an ``index.html`` file in the root.

After you upload new docs, they should show up on the Host the Docs homepage, either as a new project, or a new version.

Administration
--------------

The only administration is to remove projects or versions. Just SSH or RDP and delete the folders. A web-based interface can be added in the future, but that would probably require some security model so whatever!

FAQ
===

I'm sure you have a lot of questions. Maybe I have answers?

* Who is Host the Docs for?
  * The programmer in an enterprise environment, maybe using Windows, maybe without time or machines to spare, who has documentation to host and no good way to host it.
* Is there cross-project search?
  * No. This just hosts static HTML right now. Cross-project search is the one advanced feature I think is a no-brainer, and maybe one day Host the Docs will have it.
* What programming languages does Host the Docs support?
  * Any. Host the Docs just hosts the static HTML files generated from the programming language documentation generator of your choice.
* This project is stupid, just use *x*!
  * I wish it were so. I could not find any hosted or self-hosted solution to host documentation from private servers, such as internal source control repositories or private Github repos. My needs were so simple and the existing answers so complex, Host the Docs was born.
