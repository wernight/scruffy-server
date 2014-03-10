scruffy-server
==============

Micro web server front-end for [Scruffy](https://github.com/aivarsk/scruffy) UML.

So you have your own UML page like [yUML](http://yuml.me) and even more lean.

Screenshot
----------

![Screenshot](screenshot.png)


Installation
------------

 1. Install Scruffy pre-requisites:
      * On **Ubuntu** Linux you'd do:

            $ sudo apt-get install graphviz plotutils librsvg2-bin python-imaging

      * On **Arch** Linux you'd do:

            $ pacman -S graphviz plotutils librsvg python2-pillow

      * General: You'll need [Python](http://www.python.org/), [dot](http://www.graphviz.org/), [libRSVG](https://wiki.gnome.org/Projects/LibRsvg) binaries, [pic2plot](http://www.gnu.org/software/plotutils/), and [Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/) or [Python Pillow](http://pillow.readthedocs.org/).

 2. Install Scruffy itself:

        $ git clone https://github.com/aivarsk/scruffy.git
        $ cd scruffy
        $ virtualenv ENV --system-site-packages && source ENV/bin/activate    # (optional)
        $ python2 setup.py install    # (Scruffy doesn't work yet on Python3)
        $ suml --help
        Should display help...

 3. Run Scruffy-Server:

        $ git clone https://github.com/wernight/scruffy-server.git
        $ cd scruffy-server
        $ pip install bottle
        $ python server.py

 4. Browse [http://localhost:8080/](http://localhost:8080/)

Edit the end of `server.py` to change the port or IP binding.


Deployment
----------

Check [Bottle Deployment](http://bottlepy.org/docs/dev/tutorial.html#deployment) but be aware that
there is no ACL, no spam check, and no caching. So you probably would want it only on a private network
or proxied behind a password protected URL.


Troubleshooting FAQ
-------------------

### The UML image doesn't render properly!

Check that the user running `server.py` can execute Scruffy `suml` command.


### Text looks like blocs, Pango font Warnings!

Chech [Arch Fonts - Pango Warnings](https://wiki.archlinux.org/index.php/fonts#Pango_Warnings). You may want to install `ttf-tlwg` to have *Purisa*
and a more scruffy look (a bit like *Comic Sans*).

You can also add `..., '--font-family', 'Purisa', ...` to `suml` parameters.


### How do change the UML font and style?

Change the `check_output(...)` parameters in `server.py`.
Execute `$ suml --help` to find what is allowed.
