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
# from email_credentials import credentials
# from flask_mail import Mail
# from flask_mail import Message
from flask_cors import CORS, cross_origin
# from simulation.sim import Simulation
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

# c = credentials()
# c.setPassword()


# app.config.update(
#     DEBUG = True,
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = 465,
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = 'robert.b.shelton.42@gmail.com',
#     MAIL_PASSWORD = c.password,
# )

# mail = Mail(app)

@app.route('/s-bfls/', methods=['POST'])
@cross_origin(supports_credentials=True)
def Sbfl():
    input_data = request.get_json(force=True)
    my_s_bfl = s_bfl()
    my_s_bfl.input(input_data, sysnum = 2)
    my_s_bfl.solve()
    print(my_s_bfl.optimization_result)
    response = jsonify(my_s_bfl.optimization_result)
    my_sim = Simulation(input_data,my_s_bfl.optimization_result)
    my_sim.main()
    # response.headers.add('Access-Control-Allow-Origin', '*')

    # msg = Message('S-BFLS',
    #                 sender="robert.b.shelton.42@gmail.com",
    #                 recipients=["robes98@vt.edu"])
    # msg.body = "Thanks for using SBFLS! Attached are our results."
    # mail.send(msg)
    return response

@app.errorhandler(404)
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Note: development server only
