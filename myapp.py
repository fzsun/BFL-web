#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 21:01:11 2018

@author: Fangzhou Sun
"""

import os
import jinja2
from flask import Flask, render_template, request, send_from_directory
from algorithm.tsp import tsp

app = Flask(__name__, template_folder='')

# ============== General Page Rendering ==============
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/<path:subpath>/')
def render_static(subpath):
    """all htmls that do not need extra code in Flask"""
    return render_template(f'static_html/{subpath}.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path,'static'),'favicon.ico')

@app.errorhandler(404)
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def page_not_found(e):
    return render_template('404.html'), 404

# ============== Customized Page Rendering ==============
@app.route('/tsp/', methods=['GET', 'POST'])
def render_tsp():
    if request.method == 'POST':
        n = request.form['num_cities']
        my_tsp = tsp()
        my_tsp.from_num_cities(int(n))
        my_tsp.solve()
        result = my_tsp.all_data_
        return render_template('tsp.html', result=result)
    else:
        return render_template('tsp.html')

if __name__ == '__main__':
    app.run(debug=True, port=8081) # Note: development server only
