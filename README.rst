Welcome to Host the Docs
========================

Host the Docs is a simple way to host static code documentation.
Its main use is as a self-hosted server for your organization's private documentation.
Better alternatives are available for open source projects, such as Read the Docs or Github Pages.

Host the Docs was created after a long day of banging my head against the wall trying to get
Read the Docs set up with private GitHub repositories,
and having helped develop a plugin to get it to work with Perforce previously.
What the world needed was a way to easily host documentation from several projects,
from any source or language or SCM.

Seriously, let other people generate their own docs, I just want to Host the Docs!

Running the server
------------------

Host the Docs is built with Flask,
so it should be easy enough to set up and run,
even if you aren't a competent web programmer.
You don't even have to run Host the Docs with Apache or whatever WSGI server of your choice,
even though I recommend it since you're primarily serving static files.
::

    $ python runserver.py

That's it! Your server is using the built-in Flask webserver,
and files will be stored and served from the ``static`` directory.
Of course this sort of sucks, so let's configure our server.

Configuring the server
----------------------

Configuration is supported through environment variables or a a ``conf.py`` file
(env vars are preferred, ``conf.py`` after that, defaults after that).
The name of the environment variable is the same as the attribute in ``conf.py``
except with ``HTD_`` prepended.

The following configuration variables are probably the most useful::



Generating your docs
--------------------

Figure it out yourself!
Host the Docs uses Sphinx to generate its html documentation,
then zips up the ``build/html`` folder and sends it to a Host the Docs server.
See ``create_the_docs.py``.

Uploading your docs
-------------------

There's a single URL endpoint, ``/hmfd`` (easy to remember: "host my fucking docs").
You give it a JSON document containing some simple metadata::

    {
      "name": "Host the Docs",
      "version": "0.1.0",
      "description": "Host the Docs makes hosting any HTML documentation simple."
    }
    
And a ``.zip`` file that has an ``index.html`` file in the root.

After you upload new docs, they should show up on the Host the Docs homepage,
either as a new project, or a new version.

Administration
--------------

The only administration is to remove projects or versions.
Just SSH or RDP and delete the folders.
A web-based interface can be added in the future,
but that would probably require some security model so whatever!

FAQ
===

I'm sure you have a lot of questions. Maybe I have answers?

Who is Host the Docs for?
  The programmer in an enterprise environment, maybe using Windows,
  maybe without time or machines to spare, maybe who doesn't even do web programming,
  who has documentation to host and no good way to host it.

Is Host the Docs secure?
  Fuck no! Run it behind a firewall and only give access to people you trust.

Is Host the Docs fast?
  Fuck no! It is probably fast enough, though.
  You're probably lucky if you have more than a couple concurrent users reading your docs, anyway.

Is there cross-project search?
  No. This just hosts static HTML right now. Cross-project search
  is the one advanced feature I think is a no-brainer,
  and maybe one day Host the Docs will have it.

What programming languages does Host the Docs support?
  Any. Host the Docs just hosts the static HTML files generated from the
  programming language documentation generator of your choice.

This project is stupid, just use *x*!
  I wish it were so. I could not find any hosted or self-hosted solution to host documentation from private servers, such as internal source control repositories or private Github repos. My needs were so simple and the existing answers so complex, Host the Docs was born.

Is there a database?
  No. In the future a DB can be added if we need to cache the project information.
  I doubt we'll ever have any notion of 'users' though.
