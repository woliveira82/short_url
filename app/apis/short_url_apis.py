from datetime import datetime, timedelta
from secrets import token_urlsafe

from app import app, db
from app.models import ShortUrl
from flask import abort, jsonify, redirect, request
from flask_jwt_extended import jwt_required
from webargs import fields
from webargs.flaskparser import parser


@app.route('/short-urls', methods=['POST'])
def post_short_url():
    json = parser.parse({
        'original_url': fields.Str(required=True),
        'shorted_key': fields.Str(required=False, missing=(token_urlsafe(4))),
        'expires_at': fields.DateTime(required=False, missing=(datetime.now() + timedelta(days=7))),
    }, request)
    shorted_url = ShortUrl(**json)
    shorted_url.save()
    return jsonify(shorted_url.to_json()), 201
    

@app.route('/<shorted_key>', methods=['GET'])
def get_short_key(shorted_key):
    shorted_url = ShortUrl.query.filter_by(shorted_key=shorted_key).first_or_404()
    if shorted_url.expires_at < datetime.now():
        shorted_url.delete()
        abort(404)
    
    return redirect(shorted_url.original_url, code=302)


@app.route('/short-urls', methods=['GET'])
@jwt_required()
def get_short_url():
    query = parser.parse({
        'page': fields.Int(required=False, missing=1),
        'per_page': fields.Int(required=False, missing=20),
    }, request, location='query')
    a = ShortUrl.query.filter(ShortUrl.expires_at < datetime.now()).delete()
    db.session.commit()
    page_list = ShortUrl.query.paginate(query['page'], query['per_page'], error_out=False)
    json_response = {
        'has_next': page_list.has_next,
        'has_prev': page_list.has_prev,
        'next_num': page_list.next_num,
        'page': page_list.page,
        'pages': page_list.pages,
        'per_page': page_list.per_page,
        'prev_num': page_list.prev_num,
        'total': page_list.total,
        'items':  [ item.to_json() for item in page_list.items ],
    }
    return jsonify(json_response)
