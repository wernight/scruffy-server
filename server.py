"""
 1. Install Scruffy
 2. Run server:

        $ pip install bottle
        $ python server.py

 3. Browse http://localhost:8080/
"""
from bottle import route, run, template, request, response, BaseResponse
from optparse import Values
from subprocess import check_output
from tempfile import SpooledTemporaryFile
from urllib import quote_plus
import re
import suml.common
import suml.yuml2dot

@route('/image/')
@route('/image/<spec:path>')
def image(spec=' '):
    # Remove .png extension.
    spec = re.sub('\.png$', '', spec)

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
@route('/edit/<spec:path>')
def index(spec=''):
    spec = request.query.spec or spec
    autocollapse = True
    if not spec:
        spec = '// Cool Class Diagram,[ICustomer|+name;+email|]^-[Customer],[Customer]<>-orders*>[Order],[Order]++-0..*>[LineItem],[Order]-[note:Aggregate root.]'
        autocollapse = False

    image_url = '/image/{}.png'.format(quote_plus(
        spec.replace('\r\n', ',').replace('\r', ',').replace('\n', ',')))

    return template(
        'index.tpl',
        spec=spec.replace(',', '\n'),
        image_url=image_url,
        autocollapse=autocollapse)

if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)
