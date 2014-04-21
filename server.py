#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
"""
 1. Install Scruffy
 2. Run server:

        $ pip install bottle
        $ python server.py

 3. Browse http://localhost:8080/
"""
from bottle import route, run, template, request, response, static_file, HTTPError
import re
import reportlab.graphics
import suml.suml2pic
import suml.yuml2dot
import svglib.svglib
import urllib
import xml.dom.expatbuilder
import xml.etree.ElementTree as ET

@route('/favicon.ico')
def favicon():
    return static('favicon.ico')

@route('/robots.txt')
def robots():
    return static('robots.txt')

# Those files should be served directly by the web server,
# but for ease during development they are served here.
@route('/static/<path:path>')
def static(path):
    return static_file(path, 'static')

@route('/<type>/<spec:path>.<ext:re:png|svg|pdf>')
def image(type, spec=' ', ext='png'):

    # Parameters for `suml`.
    import suml.common
    import optparse
    options = optparse.Values(({
        'scruffy': True,
        'png': ext == 'png',
        'svg': ext == 'svg' or ext == 'pdf',
        'font': suml.common.defaultScruffyFont(),
        'shadow': False,
    }))

    from tempfile import SpooledTemporaryFile
    fout = SpooledTemporaryFile()

    # Execute Scruffy `suml`.
    if type == 'class':
        suml.yuml2dot.transform(spec, fout, options)
    elif type == 'sequence':
        suml.suml2pic.transform(spec, fout, options)
    else:
        return HTTPError(404, 'Unhandled diagram type.')

    # Retrieve the data generated.
    fout.seek(0)
    data = fout.read()
    fout.close()

    # Convert SVG to PDF?
    if ext == 'pdf':
        # Load SVG file.
        doc = xml.dom.expatbuilder.parseString(data)

        # Convert to a RLG drawing
        svg_renderer = svglib.svglib.SvgRenderer()
        svg_renderer.render(doc.documentElement)
        drawing = svg_renderer.finish()

        # Generate PDF.
        data = reportlab.graphics.renderPDF.drawToString(drawing)

    # Server the generated image.
    if ext == 'png':
        response.content_type = 'image/png'
    elif ext == 'svg':
        response.content_type = 'image/svg+xml'
    elif ext == 'pdf':
        response.content_type = 'application/pdf'
    else:
        return HTTPError(500, 'Unhandled extension type.')
    return data

@route('/')
def index():
    return template('home.tpl')

@route('/<type>/')
@route('/<type>/<spec:path>')
def index(type='class', spec=''):
    spec = request.query.spec or spec

    if type != 'class' and type != 'sequence':
        return HTTPError(404, 'Unhandled diagram type.')

    autocollapse = True
    if not spec:
        if type =='class':
            spec = '// Cool Class Diagram,[ICustomer|+name;+email|]^-.-[Customer],[Customer]<>-orders*>[Order],[Order]++-0..*>[LineItem],[Order]-[note:Aggregate root.]'
        elif type == 'sequence':
            spec = '[Patron]order food>[Waiter],[Waiter]order food>[Cook],[Waiter]serve wine>[Patron],[Cook]pickup>[Waiter],[Waiter]serve food>[Patron],[Patron]pay>[Cashier]'
        else:
            return HTTPError(404, 'Unhandled diagram type.')
        autocollapse = False

    encoded_spec = urllib.quote_plus(spec.replace('\r\n', ',').replace('\r', ',').replace('\n', ','))

    return template(
        'index.tpl',
        type=type,
        spec=spec.replace(',', '\n'),
        encoded_spec=encoded_spec,
        autocollapse=autocollapse)

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)
