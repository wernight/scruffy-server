scruffy-server
==============

Micro web server front-end for [Scruffy](https://github.com/aivarsk/scruffy) UML.

So you have your own UML page like yUML and even more lean.

Installation
------------

  1. Install Scruffy, for Ubuntu you'd do:

          $ sudo apt-get install git librsvg2-bin plotutils graphviz
          $ git clone https://github.com/aivarsk/scruffy.git
          $ cd scruffy
          $ virtualenv ENV --system-site-packages && source ENV/bin/activate       # (optional)
          $ python setup.py install

  2. Run server:

          $ git clone https://github.com/wernight/scruffy-server.git
          $ cd scruffy-server
          $ pip install bottle
          $ python server.py

  3. Browse http://localhost:8080/

Deployment
----------

Check [Bottle Deployment](http://bottlepy.org/docs/dev/tutorial.html#deployment) but be aware that
there is no ACL, no spam check, and no caching. So you probably would want it only on a private network
or proxied behind a password protected URL.

To Do
-----

  * Detect and report invalid UML inputs.

