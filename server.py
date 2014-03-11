"""
 1. Install Scruffy
 2. Run server:

        $ pip install bottle
        $ python server.py

 3. Browse http://localhost:8080/

TODO: Detect and report invalid UML inputs.
"""
from bottle import route, run, template, response, BaseResponse
from optparse import Values
from subprocess import check_output
from tempfile import SpooledTemporaryFile
import suml.common
import suml.yuml2dot

@route('/image/')
@route('/image/<spec:path>')
def image(spec=' '):
    spec = spec.replace('\n', ',')
    fout = SpooledTemporaryFile()

    # Execute Scruffy `suml`.
    options = Values(({
        'scruffy': True,
        'font': suml.common.defaultScruffyFont(),
        'png': True,
        'shadow': False,
    }))
    suml.yuml2dot.transform(spec, fout, options)

    fout.seek(0)
    png = fout.read()
    fout.close()

    # Server the generated image.
    response.content_type = 'image/png'
    return png

@route('/')
@route('/edit/')
@route('/edit/<uml:path>')
def index(uml='// Cool Class Diagram,[ICustomer|+name;+email|]^-[Customer],[Customer]<>-orders*>[Order],[Order]++-0..*>[LineItem],[Order]-[note:Aggregate root.]'):
    uml = uml.replace(',', '\n')
    return template("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Scruffy</title>
            <script type="text/javascript" src="//code.jquery.com/jquery-2.1.0.min.js"></script>
            <script type="text/javascript" src="//code.jquery.com/ui/1.10.4/jquery-ui.min.js"></script>
            <link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
            <style>
            form {
                display: inline-block;
            }
            textarea {
                background: #ffe;
            }
            img {
                vertical-align: top;
            }
            </style>
        </head>
        <body>
            <form>
                <textarea name="uml" rows="10" cols="80" autofocus="autofocus">{{uml}}</textarea>
                <div>See <a href="https://github.com/aivarsk/scruffy/blob/master/README.rst" target="_blank">Scruffy syntax</a>.</div>
            </form>
            <a href="#" title="Click to edit"><img src="" /></a>
            <script type="text/javascript">
            var umlTextarea = $('textarea');
            var umlImage = $('img');

            // Update when the input text is changed (after a short delay).
            (function() {
              var update = function() {
                var spec = umlTextarea.val().replace(/(\\r\\n|\\n|\\r)/gm, ',');
                var specUri = encodeURIComponent(spec);
                umlImage.attr('src', '/image/' + specUri);

                // Change the current URL after unencoding some pretty safe characters.
                specUri = specUri.replace('%5B', '[').replace('%5D', ']');
                specUri = specUri.replace('%3C', '<').replace('%3E', '>');
                specUri = specUri.replace('%7B', '{').replace('%7D', '}');
                specUri = specUri.replace('%2F', '/');
                specUri = specUri.replace('%26', '&');
                specUri = specUri.replace('%2B', '+');
                specUri = specUri.replace('%2C', ',');
                specUri = specUri.replace('%3A', ':');
                specUri = specUri.replace('%3B', ';');
                specUri = specUri.replace('%3D', '=');
                specUri = specUri.replace('%24', '$');
                specUri = specUri.replace('%40', '@');
                specUri = specUri.replace('%7C', '|');

                window.history.pushState('Scruffy', 'Scruffy', '/edit/' + specUri);
              };
              var delay = (function() {
                var timer = 0;
                return function(callback, ms) {
                  clearTimeout (timer);
                  timer = setTimeout(callback, ms);
                };
              })();
              umlTextarea.on('input', function() {
                delay(update, 300);
              });
              update();
            })();

            // Show/hide the input textarea.
            (function() {
              var inputForm = $('form');

              var show = function() {
                inputForm.slideDown(200);
                umlTextarea.focus();
                return false;
              };

              var hide = function() {
                // If the UML was successfully generated, hide the image.
                if (umlImage.width() + umlImage.height() > 50) {
                  inputForm.slideUp(200);
                }
              };

              // Limit the textarea size.
              umlTextarea.resizable({
                minHeight: 100,
                minWidth: 300,
                handles: 'se'
              }).parent().css('padding-bottom', '0');

              // Toggle display input on click image.
              umlImage.click(function() {
                if (inputForm.is(':visible')) {
                  hide();
                } else {
                  show();
                }
                return false;
              });

              // Display input on key press.
              $('html').keypress(function(e) {
                show();
              });

              // Hide on key ESC, show on arrow keys.
              $('html').keydown(function(e) {
                if (e.keyCode == 27) {
                  hide();
                } else if (e.keyCode >= 37 && e.keyCode <= 40) {
                  show();
                }
              });

              // Hide input when clicking outside.
              $('html').click(function() {
                hide();
              });
              umlTextarea.click(function() {
                return false;
              });

              hide();
            })();
            </script>
        </body>
        </html>
        """,
        uml=uml)

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)
