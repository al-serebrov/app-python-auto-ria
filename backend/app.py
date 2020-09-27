import datetime
import os
from copy import deepcopy

import requests
from flask import Flask, jsonify, request

from autoria.api import RiaAPI, RiaAverageCarPriceParams
from flask_cors import CORS
from urllib.parse import urlencode

app = Flask(__name__)
# unsafe, all origins have access, should be limited to frontend
CORS(app, resources={r"/*": {"origins": "*"}}, max_age=3600)
ria_api = RiaAPI()
api_key = os.environ.get('API_KEY')
new_api_url = 'https://developers.ria.com/auto/{method}'


# a simple page that says hello
@app.route('/')
def hello():
    return "Hello World!"


@app.route('/categories')
def categories():
    return jsonify(ria_api.get_categories())


@app.route('/categories/<category_id>/bodystyles')
def bodystyles(category_id):
    return jsonify(ria_api.get_bodystyles(category_id))


@app.route('/categories/<category_id>/marks')
def marks(category_id):
    return jsonify(ria_api.get_marks(category_id))


@app.route('/categories/<category_id>/gearboxes')
def gearboxes(category_id):
    return jsonify(ria_api.get_gearboxes(category_id))


@app.route('/categories/<category_id>/driverTypes')
def driver_types(category_id):
    return jsonify(ria_api.get_driver_types(category_id))


@app.route('/categories/<category_id>')
def category_info(category_id):
    return jsonify({
        'bodystyles': ria_api.get_bodystyles(category_id),
        'marks': ria_api.get_marks(category_id),
        'gearboxes': ria_api.get_gearboxes(category_id),
        'driverTypes': ria_api.get_driver_types(category_id),
    })


@app.route('/categories/<category_id>/marks/<mark_id>/models')
def models(category_id, mark_id):
    return jsonify(ria_api.get_models(category_id, mark_id))


@app.route('/states')
def states():
    return jsonify(ria_api.get_states())


@app.route('/states/<state_id>/cities')
def cities(state_id):
    return jsonify(ria_api.get_cities(state_id))


@app.route('/fuels')
def fuels():
    return jsonify(ria_api.get_fuels())


@app.route('/colors')
def colors():
    return jsonify(ria_api.get_colors())


@app.route('/average')
def average():
    args = deepcopy(dict(request.args))
    args['api_key'] = api_key
    start_year = args.get('startYear', '1900')
    end_year = args.get('endYear', datetime.datetime.now().year)
    years = [start_year, end_year]
    ria_parameters = RiaAverageCarPriceParams(
        api_key=api_key,
        main_category=args.get('category'),
        marka_id=args.get('mark'),
        model_id=args.get('model'),
        state_id=args.get('state'),
        body_id=args.get('bodystyle'),
        city_id=args.get('city'),
        yers=years,
        gear_id=process_multiple_values(args.get('gears', '')),
        fuel_id=process_multiple_values(args.get('fuels', '')),
        color_id=args.get('color'),
        # TODO:
        raceInt=None,
        options=None,
        drive_id=None,
        engineVolume=None,
        seats=None,
        door=None,
        carrying=None,
        custom=None,
        damage=None,
        under_credit=None,
        confiscated_car=None,
        onRepairParts=None,
    )
    params = {k: v for (k, v) in ria_parameters._asdict().items() if v}
    query = urlencode(params, doseq=True)
    req_url = new_api_url.format(method='average_price?{}'.format(query))
    response = requests.get(url=req_url)
    if response.status_code == 200:
        return jsonify(response.text)
    else:
        raise Exception(
            'Error making a request to: {}, response: {}, {}'
            .format(req_url, response.status_code, response.text))


def process_multiple_values(value):
    if ',' in value:
        return value.split(',')
    return value


@app.route('/classifieds/<classified_id>')
def classified_info(classified_id):
    req_url = new_api_url.format(method='info')
    params = {
        'api_key': api_key,
        'auto_id': classified_id
    }
    response = requests.get(url=req_url, params=params)
    if response.status_code == 200:
        return jsonify(response.text)
    else:
        raise Exception(
            'Error making a request to: {}, response: {}, {}'
            .format(req_url, response.status_code, response.text))
