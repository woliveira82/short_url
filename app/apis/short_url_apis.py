from datetime import datetime, timedelta
from secrets import token_urlsafe

from app import app
from app.models import ShortUrl
from flask import abort, jsonify, redirect, request
from webargs import fields
from webargs.flaskparser import parser


@app.route('/short-urls', methods=['POST'])
def post_short_url():
    json = parser.parse({
        'original_url': fields.Str(required=True),
        'shorted_key': fields.Str(required=False, missing=(token_urlsafe(4))),
        'expires_at': fields.DateTime(required=False, missing=(datetime.now() + timedelta(days=7))),
    }, request)
    json['shorted_key'] = app.config['DOMAIN_BASE_URL'] + json['shorted_key']
    shorted_url = ShortUrl(**json)
    shorted_url.save()
    return jsonify(shorted_url.to_json())
    

@app.route('/<shorted_key>', methods=['GET'])
def get_short_url(shorted_key):
    shorted_url = ShortUrl.query.filter_by(shorted_key=shorted_key).first()
    if not shorted_url:
        abort(404)
    
    return redirect(shorted_url.original_url, code=302)
