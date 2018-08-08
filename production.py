#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 21:01:11 2018

@author: Fangzhou Sun
"""

from waitress import serve # production server
import myapp

if __name__ == '__main__':
    serve(myapp.app, listen='*:8081') 