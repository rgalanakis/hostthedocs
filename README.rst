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

See the ``conf.py.template`` file for a list and explanation of all the
configuration values Host the Docs supports.

Generating your docs
--------------------

Figure it out yourself!
For example, you can use Sphinx to generate html documentation (``make html``),
then zip up the ``build/html`` folder and send it to a Host the Docs server
via POSTing to ``/hmfd`` (see next section).

Uploading your docs
-------------------

There's a single URL endpoint, ``/hmfd`` (easy to remember: "host my fucking docs").
Just POST a JSON document containing some simple metadata::

    {
      "name": "Host the Docs",
      "version": "0.1.0",
      "description": "Host the Docs makes hosting any HTML documentation simple."
    }
    
and a ``.zip`` file that has an ``index.html`` file in the root.
The ``'name'`` key must contain only letters, numbers, spaces, underscores, and dashes.
The ``version`` must contain only letters, numbers, and periods.
The ``description`` can be any string, and can contain HTML.

After you upload new docs, they should show up on the Host the Docs homepage,
either as a new project, or a new version.

See ``host_my_docs.py`` for an example script that uses the ``requests`` library
to make a successful ``/hmfd`` POST.

Deleting your docs
------------------

You can DELETE to the ``/hmfd`` endpoint to delete a version or entire project.
Use the URL to delete the project name and version and it will be delete if it exists.
For example, the following command will delete version 1.2 of MyProject's docs::

    curl -X DELETE "http://127.0.0.1:5000/hmfd?name=MyProject&version=1.2"

If the last version is deleted, the project will still remain
(this is by design, is it a good one?).
You need to include include a ``"entire_project"`` key to remove the entire project,
including all versions, removing the display of the project entirely
(note you do not need to include the version).::

    curl -X DELETE "http://127.0.0.1:5000/hmfd?name=MyProject&entire_project=True"

Alternatively, you can just ssh or RDP into the host and delete the directories yourself.

Obviously there's no security here.
On the other hand, it isn't exposed through any UI,
so it's not like some random person is going to stumble across it
or accidentally press a button.
And you can always regenerate the docs easily if something happened.

FAQ
===

I'm sure you have a lot of questions. Maybe I have answers?

Who is Host the Docs for?
  The programmer in an enterprise environment,
  maybe using Windows,
  maybe without time or machines to spare,
  maybe who doesn't even do web programming,
  who has documentation to host and no good way to host it.
  If you really hate Host the Docs,
  and find its ideas and implementation offensive,
  it's probably not for you.

Is Host the Docs secure?
  No. Run it behind a firewall and only give access to people you don't mistrust
  (ie, only people within your organization, not the general public).
  It does some basic validation of things like project names and versions,
  but there are all sorts of holes.

Is Host the Docs fast?
  No. It is probably fast enough, though.
  You're probably lucky if you have more than a couple concurrent users reading your docs, anyway.

Is there cross-project search?
  No. This just hosts static HTML right now.
  The search *within* a project should work,
  but you cannot search across projects.
  I'd love to add it, but as I've never done something like this before,
  it'd probably be more work than I can commit to.
  If you're interested in adding this feature, please email me!

What programming languages does Host the Docs support?
  Any. Host the Docs just hosts the static HTML files generated from the
  programming language documentation generator of your choice.

This project is stupid, just use **x**!
  I wish it were so. I could not find any hosted or self-hosted solution to
  host documentation from private servers,
  such as internal source control repositories or private Github repos.
  My needs were so simple and the existing answers so complex,
  Host the Docs was born.

Is there a database?
  No. In the future a DB can be added if we need to cache the project information.
  I doubt we'll ever have any notion of 'users' though.

Is Host the Docs' theme customizable?
  No, at least not right now. I'd like to get some more users first.
  The "site" is a single page, so I'm not sure it's worth it.
  The two options are to configure where Flask serves its static files from
  (so you would provide a whole new template),
  or make the current colors configurable,
  maybe through some inline stylesheets that are templated through config values.
  Not sure. Open to ideas.

Does Host the Docs support images?
  No, at least right now. I want to avoid complicating things at first.
  I'd like to add project images, maybe,
  and of course a logo/favicon for Host the Docs itself.
  You can embed an ``<img>`` tag in your project description HTML,
  if you really want.
