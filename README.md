[![](https://images.microbadger.com/badges/image/wernight/scruffy-server.svg)](http://microbadger.com/images/wernight/scruffy-server "Get your own image badge on microbadger.com") [![Codenvy badge](http://beta.codenvy.com/factory/resources/codenvy-contribute.svg)](http://beta.codenvy.com/f?url=https://github.com/wernight/scruffy-server 'Start development server on Codenvy')

**scruffy-server** is a micro web server front-end for [Scruffy](https://github.com/aivarsk/scruffy): A UML class/sequence diagram generator from human text, like yUML, with a very clean interface.

Features:

 * UML Class diagram
 * UML Sequence diagram
 * PNG / SVG export
 * Simple and fast interface
 * Works also without JavaScript
 * Mobile friendly


### Screenshots

![Screenshot](https://github.com/wernight/scruffy-server/raw/master/screenshot.png)

![Screenshot Mobile](https://github.com/wernight/scruffy-server/raw/master/screenshot-mobile.png)


### Installation


#### Using Docker

If you have [Docker](https://www.docker.com/) installed:

    $ docker run -d -p 8080:8080 wernight/scruffy-server

And browse to [http://localhost:8080/](http://localhost:8080/)

That Dockerize container is:

  * **Small**: Using [Debian image][debian] is below 100 MB (while Ubuntu is about 230 MB), and removing build packages.
  * **Simple**: Exposes default port, easy to extend.
  * **Secure**: Runs as non-root UID/GID `35726` (selected randomly to avoid mapping to an existing user).


##### Deploy for Production

You can deploy on Kubernetes (for example on Google Container Engine), once you've kubectl and a running cluster:

    $ kubectl run-container scruffy --image=wernight/scruffy-server:latest --port=80
    $ kubectl expose rc scruffy --port=80 --target-port=8080 --create-external-load-balancer

Wait may be a minute or so and you should have a public IP (the second one here):

    $ kubectl get svc scruffy
    NAME      LABELS        SELECTOR      IP(S)           PORT(S)
    scruffy   run=scruffy   run=scruffy   10.255.255.10   80/TCP
                                          104.123.45.67
    $ xdg-open http://104.123.45.67

Be aware that there is no ACL, no spam check, and no caching (i.e. anyone can access by default and evil doers might use all your CPU). So you probably would want it only on a private network or proxied behind a password protected URL. For example you could put it behind Nginx as reverse proxy, with a basic authentication.


#### Manual Install

 1. Install Scruffy pre-requisites:
      * On **Ubuntu** Linux you'd do:
        `$ sudo apt-get install python-dev python-setuptools graphviz plotutils librsvg2-bin`
      * On **Arch** Linux you'd do:
        `$ pacman -S graphviz python2 plotutils librsvg`
      * In *general*: You'll need [Python](http://www.python.org/), [dot](http://www.graphviz.org/), [libRSVG](https://wiki.gnome.org/Projects/LibRsvg) binaries, [pic2plot](http://www.gnu.org/software/plotutils/), and [Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/) or [Python Pillow](http://pillow.readthedocs.org/).
 2. Run Scruffy-Server:

        $ git clone https://github.com/wernight/scruffy-server.git
        $ cd scruffy-server
        $ virtualenv ENV --system-site-packages && source ENV/bin/activate    # (optional)
        $ pip install -r requirements.txt
        $ python server.py

 3. Browse [http://localhost:8080/](http://localhost:8080/)

Edit the end of `server.py` to change the port or IP binding.

See also [Bottle Deployment](http://bottlepy.org/docs/dev/tutorial.html#deployment).


### Similar Tools

  * [yUML](http://yuml.me) Which is very similar commercial alternative, with Use Case, Activity, and Class diagram support (and not a so great mobile support).
  * [PlantUML](http://plantuml.sourceforge.net/) An OpenSource Java solution, also text based which supports most UML diagrams with a more classic look (and not a so great mobile support).
  * [nomnoml](http://www.nomnoml.com/) A UML class diagram using JavaScript (only).
  * [draw.io](https://www.draw.io/) and [Lucidchart](https://www.lucidchart.com/) are also online solutions but not auto-generated from text.

*scruffy-server* is good for lean short UML diagrams even from a mobile phone or tablet.


### Troubleshooting FAQ

#### Why is there no password protection or ACL?

The only real risk is that your server isn't well **sandboxed** and a user sends malicious UML code.

For users however there is **no real need for password** protection because the URL shared is the entire UML diagram source code.
This means that no one can try to guess your UML by trying random URLs (as it would only generate all possible UMLs),
and any change to an existing UML will generate a new URL. So you can generate a diagram, share it, without
ever needing a password. **Just remember: URL = UML.**


#### The UML image doesn't render properly!

Check that the user running `server.py` can execute Scruffy `suml` command.


#### Text looks like blocs, Pango font Warnings!

Chech [Arch Fonts - Pango Warnings](https://wiki.archlinux.org/index.php/fonts#Pango_Warnings). You may want to install `ttf-tlwg` to have *Purisa*
and a more scruffy look (a bit like *Comic Sans*).

You can also add `..., '--font-family', 'Purisa', ...` to `suml` parameters, see "How to change the UML font and style" question below.


#### How to change the UML font and style?

If you just want to use another font, you can set environement variable `SCRUFFY_FONT` to the font family you'd like to use.

For a full list of possible settings, execute `$ suml --help` to find what is allowed and change the `check_output(...)` parameters in `server.py`.


### Feedbacks

Improvement ideas and pull requests are welcome via
[Github Issue Tracker](https://github.com/wernight/scruffy-server/issues).
