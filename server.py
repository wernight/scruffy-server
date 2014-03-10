"""
 1. Install Scruffy
 2. Run server:

        $ pip install bottle
        $ python server.py

 3. Browse http://localhost:8080/

TODO: Detect and report invalid UML inputs.
"""
from bottle import route, run, template, response, BaseResponse
from subprocess import check_output

@route('/image/<uml:path>')
def suml(uml):
    uml = uml.replace('\n', ',')
    png = check_output(['suml', '--scruffy', '--png', uml])
    response.content_type = 'image/png'
    return png

@route('/')
@route('/edit/<uml:path>')
def index(uml='// Cool Class Diagram,[ICustomer|+name;+email|]^-[Customer],[Customer]<>-orders*>[Order],[Order]++-0..*>[LineItem],[Order]-[note:Aggregate root.]'):
    uml = uml.replace(',', '\n')
    return template("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Scruffy</title>
            <style>
            form {
                display: inline-block;
            }
            textarea {
                min-width: 300px;
                width: 800px;
                height: 300px;
                background: #ffe;
            }
            img {
                vertical-align: top;
            }
            </style>
        </head>
        <body>
            <form>
                <textarea name="uml" autofocus="autofocus">{{uml}}</textarea>
                <div>See <a href="https://github.com/aivarsk/scruffy/blob/master/README.rst" target="_blank">Scruffy syntax</a>.</div>
            </form>
            <a href="#" title="Click to edit"><img src="" /></a>
            <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.0/jquery.js"></script>
            <script type="text/javascript">
            // Update when the input text is changed (after a short delay).
            var update = function() {
              var uml = $('textarea').val().replace(/(\\r\\n|\\n|\\r)/gm, ',');
              $('img').attr('src', '/image/' + encodeURIComponent(uml));
              window.history.pushState('Scruffy', 'Scruffy', '/edit/' + encodeURIComponent(uml));
            };
            var delay = (function() {
              var timer = 0;
              return function(callback, ms){
                clearTimeout (timer);
                timer = setTimeout(callback, ms);
              };
            })();
            $('textarea').on('input', function() {
              delay(update, 300);
            });

            var show = function() {
              $('form').slideDown(200);
              $('textarea').focus();
              return false;
            };

            var hide = function() {
              $('form').slideUp(200);
            };

            // Display input on click.
            $('img').click(show);

            // Display input on key down, except ESC.
            $('html').keydown(function(e) {
              if (e.keyCode == 27) {
                hide();
              } else {
                show();
              }
            });

            // Hide input when clicking outside.
            $('html').click(function() {
              hide();
            });
            $('textarea').click(function() {
              return false;
            });

            update();
            hide();
            </script>
        </body>
        </html>
        """,
        uml=uml)

run(host='localhost', port=8080)
