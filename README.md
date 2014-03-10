scruffy-server
==============

Micro web server front-end for [Scruffy](https://github.com/aivarsk/scruffy) UML.

So you have your own UML page like yUML and even more lean.

![Screen-shot](screenshot.png)


Installation
------------

 1. Install Scruffy pre-requisites:
      * On **Ubuntu** Linux you'd do:

            $ sudo apt-get install graphviz plotutils librsvg2-bin python-imaging

      * On **Arch** Linux you'd do:

            $ pacman -S graphviz plotutils librsvg python2-pillow

 2. Install Scruffy itself:

        $ git clone https://github.com/aivarsk/scruffy.git
        $ cd scruffy
        $ virtualenv ENV --system-site-packages && source ENV/bin/activate    # (optional)
        $ python2 setup.py install    # (Scruffy doesn't work yet on Python3)
        $ suml --help
        Should display help...

 2. Run this server:

        $ git clone https://github.com/wernight/scruffy-server.git
        $ cd scruffy-server
        $ pip install bottle
        $ python server.py

  3. Browse http://localhost:8080/

Edit the end of `server.py` to change the port or IP binding.


FAQ
---

### The UML image doesn't render properly!

Check that the user running `server.py` can execute Scruffy `suml` command.

### How do change the stype?

Change the `check_output(...)` parameters in `server.py`.
Execute `$ suml --help` to find what is allowed.

### Text looks like blocs, fonts are all wrong, Pango Warnings!

Chech [Arch Fonts - Pango Warnings](https://wiki.archlinux.org/index.php/fonts#Pango_Warnings). You may want to install `ttf-tlwg` to have *Purisa*
and a more scruffy look (a bit like *Comic Sans*).

You can also add a `..., '--font-family', 'Purisa', ...` command-line parameter.


Deployment
----------

Check [Bottle Deployment](http://bottlepy.org/docs/dev/tutorial.html#deployment) but be aware that
there is no ACL, no spam check, and no caching. So you probably would want it only on a private network
or proxied behind a password protected URL.


To Do
-----

  * Detect and report invalid UML inputs.

