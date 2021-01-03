import json
import sys
from peewee import (
    fn,
    JOIN,
    SQL,
    DoesNotExist,
    IntegrityError
)

from playhouse.shortcuts import model_to_dict, dict_to_model

from flask import Blueprint, jsonify, current_app, request, g
from flask_restful import inputs

sys.path.insert(0, '..')

from models import *
from api_exceptions import NoSuchData

bp_ingredients = Blueprint(
    name='ingredients',
    import_name=__name__,
    url_prefix='/ingredients'
)

@bp_ingredients.route('/', methods=['GET', 'POST'])
def handle_ingredients():
    if request.method == 'GET':
        query = (
            IngredientDimension
                .select()
                .execute()
        )
        ingredients_arr = {
            n.ingredient: model_to_dict(n) for n in query
        }
        return json.dumps(ingredients_arr), 200

    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Parser requires JSON format."}), 415

        try:
            with g.db.atomic():
                req_json = request.get_json()

                batch_size = 50
                for idx in range(0, len(req_json), batch_size):
                    current_app.logger.info(f"Inserting rows {idx} to {idx + batch_size}")
                    rows = req_json[idx:idx + batch_size]

                    for r in rows:
                        r['included_in_delivery'] = inputs.boolean(r['included_in_delivery'])

                    IngredientDimension.insert_many(rows).execute()

            return jsonify({
                "message": f"Added {len(req_json)} new ingredient(s)."
            }), 201

            f"Added {len(req_json)} new ingredient(s).", 201
        except Exception as e:
            current_app.logger.error(sys.exc_info())
            return str(e), 400

