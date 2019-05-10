#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 21:01:11 2018

@author: Fangzhou Sun
"""

import os
import jinja2
from flask import Flask, render_template, request, send_from_directory, jsonify, send_file
from algorithm.tsp import tsp
from algorithm.s_bfl import s_bfl
from flask_cors import CORS, cross_origin
from algorithm.geo import Geo
from simulation.sim import Simulation
import json

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)  # This replaces your existing "app = Flask(__name__)"
CORS(app, supports_credentials = True)

my_sim = Simulation()

@app.route('/s-bfls/', methods=['POST'])
@cross_origin(supports_credentials=True)
def Sbfl():
    input_data = request.get_json(force=True)

    # Intialize instance of s_bfl class which contains
    # Gurobipy optimization logic
    my_s_bfl = s_bfl()
    # use class input method to load data in instance
    my_s_bfl.input(input_data, sysnum = 2)
    # run the Gurobi model
    my_s_bfl.solve()
    print(my_s_bfl.optimization_result)

    # create response dictionary that will be converted to
    # JSON and returned to frontend as response payload
    response_dict = dict()
    response_dict['op_response'] = my_s_bfl.optimization_result

    # run simulation with result of optimization and orginal
    # user created data
    my_sim.new_input(input_data,my_s_bfl.optimization_result)
    my_sim.main()

    # store result
    response_dict['sim_response'] = my_sim.sim_results
    response = jsonify(response_dict)

    # send to frontend
    return response

@app.errorhandler(404)
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Note: development server only
