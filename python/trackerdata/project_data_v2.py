#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:09:13 2017

@author: ntelford
"""

import json
from project import Project


# Data handling
API_KEY = "1b75e51e0a719691c6f08e2e9f884fe9"  # NT

#  full list so far
'''  project_ids = [1363324,1560807,1491090,1861211,1452016,1892181,
                  1914447,1915901,1991111,1990717,1966499,1959473,
                  1954553,1953521,1946955,1946573,1934631,1930699,
                  1928679,1906101,1763881,1662777,1626911,1613383,
                  1608471,1610633,1598663,1593327,1592693,1591495,
                  1583707,1573253,1562257,875389,1551801,1546135,
                  1500356,1488234,1485598,1479414,1476104,1443654,
                  1389034,1378418,1364826,1362630,1244670,1233184,
                  1220370,1212538,1203638,1203634,1194374,1126018,
                  1011254,975916,957004,954118,946120,939266,930980,
                  923920,875389,849813,803319,625235,555129,254145]
'''

project_ids = [1861211]
projects = {}


def export_activity():
    for pid, project in projects.items():
        data = {}
        data['project_info'] = project.project_info
        data['activity'] = project.activity
        f = open("./project_data/project_%(pid)d.json" % {"pid": pid}, 'w')
        json.dump(data, f)
        f.close()


def api_all():
    '''Download activity data from Tracker for all projects in project_ids'''

    for pid in project_ids:
        try:
            import_from_api(pid)
        except:
            raise


def import_from_api(pid):
    '''Download all activity from the Tracker API for project pid'''

    print('Downloading activity for ' + str(pid))
    projects[pid] = Project(pid)
    projects[pid].get_project_data(API_KEY)


def json_all():
    '''Load activity data from JSON file for all projects in project_ids'''

    for pid in project_ids:
        try:
            import_from_json(pid)
        except:
            raise


def import_from_json(pid):
    '''Load activity data from JSON file for project pid'''

    print("Importing %(pid)d JSON" % {"pid": pid})
    with open(
            "./project_data/project_%(pid)d.json" % {"pid": pid},
            'r'
            ) as f:
        projects[pid] = Project(pid)
        data = json.load(f)
        projects[pid].activity = data['activity']
        projects[pid].project_info = data['project_info']
        projects[pid]._parse_stories()
