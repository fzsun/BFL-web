#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 21:01:11 2018

@author: Fangzhou Sun
"""

import os
import jinja2
from flask import Flask, render_template, request, send_from_directory, jsonify
from algorithm.tsp import tsp
from algorithm.s_bfl import s_bfl

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__,template_folder='')  # This replaces your existing "app = Flask(__name__)"

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

# ============== Page Rendering ==============
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/<path:subpath>/')
def static_html(subpath):
    """all htmls that do not need extra code in Flask"""
    return render_template(f'static_html/{subpath}.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path,'static'),'favicon.ico')

@app.route('/s-bfl/', methods=['POST'])
def Sbfl():
    input_data = request.get_json(force=True)
    my_s_bfl = s_bfl()
    my_s_bfl.input(input_data, sysnum = 2)
    my_s_bfl.solve()
    print(my_s_bfl.optimization_result)
    return jsonify(my_s_bfl.optimization_result)

@app.errorhandler(404)
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def page_not_found(e):
    return render_template('404.html'), 404

# ============== POST Actions ==============
@app.route('/tsp/action/', methods=['POST'])
def render_tsp():
    json_data = request.get_json(force=True)
    n = json_data['num_cities']
    my_tsp = tsp()
    my_tsp.from_num_cities(int(n))
    my_tsp.solve()
    return jsonify(my_tsp.all_data_)

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Note: development server only

    
