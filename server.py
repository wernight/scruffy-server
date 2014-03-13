"""
 1. Install Scruffy
 2. Run server:

        $ pip install bottle
        $ python server.py

 3. Browse http://localhost:8080/
"""
from bottle import route, run, template, request, response, HTTPError
from optparse import Values
from subprocess import check_output
from tempfile import SpooledTemporaryFile
from urllib import quote_plus
import re

@route('/<type>/<spec:path>.<ext:re:png|svg>')
def image(type, spec=' ', ext='png'):

    # Parameters for `suml`.
    import suml.common
    options = Values(({
        'scruffy': True,
        'png': ext == 'png',
        'svg': ext == 'svg',
        'font': suml.common.defaultScruffyFont(),
        'shadow': False,
    }))

    fout = SpooledTemporaryFile()

    # Fix a bug in Scruffy (for sequence diagram).
    suml.common._boxes = {}

    # Execute Scruffy `suml`.
    if type == 'class':
        import suml.yuml2dot
        suml.yuml2dot.transform(spec, fout, options)
    elif type == 'sequence':
        import suml.suml2pic
        suml.suml2pic.transform(spec, fout, options)
    else:
        return HTTPError(404, 'Unhandled diagram type.')

    fout.seek(0)
    data = fout.read()
    fout.close()

    # Server the generated image.
    if ext == 'png':
        response.content_type = 'image/png'
    elif ext =='svg':
        response.content_type = 'image/svg+xml'
    else:
        return HTTPError(500, 'Unhandled extension type.')
    return data

@route('/')
@route('/<type>/')
@route('/<type>/<spec:path>')
def index(type='class', spec=''):
    spec = request.query.spec or spec

    if type != 'class' and type != 'sequence':
        return HTTPError(404, 'Unhandled diagram type.')

    autocollapse = True
    if not spec:
        if type =='class':
            spec = '// Cool Class Diagram,[ICustomer|+name;+email|]^-[Customer],[Customer]<>-orders*>[Order],[Order]++-0..*>[LineItem],[Order]-[note:Aggregate root.]'
        elif type == 'sequence':
            spec = '[Patron]order food>[Waiter],[Waiter]order food>[Cook],[Waiter]serve wine>[Patron],[Cook]pickup>[Waiter],[Waiter]serve food>[Patron],[Patron]pay>[Cashier]'
        else:
            return HTTPError(404, 'Unhandled diagram type.')
        autocollapse = False

    encoded_spec = quote_plus(spec.replace('\r\n', ',').replace('\r', ',').replace('\n', ','))

    return template(
        'index.tpl',
        type=type,
        spec=spec.replace(',', '\n'),
        encoded_spec=encoded_spec,
        autocollapse=autocollapse)

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)
