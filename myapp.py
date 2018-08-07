#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 21:01:11 2018

@author: Fangzhou Sun
"""

from flask import Flask, render_template, request
from algorithm.tsp import tsp

app = Flask(__name__, template_folder='')

@app.route('/tsp/', methods=['GET', 'POST'])
def render_tsp():
    if request.method == 'POST':
        n = request.form['num_cities']
        my_tsp = tsp()
        my_tsp.from_num_cities(int(n))
        my_tsp.solve()
        my_tsp.dump()
        return render_template('tsp.html', result=my_tsp.obj_, default_value=n)
    else:
        return render_template('tsp.html')

@app.route('/')
def root():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8081)
