# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 09:42:11 2017

@author: ntelford
"""

import json
from project import Project
import datetime as dt
from bokeh.plotting import show, output_file
from bokeh.charts import Scatter, BoxPlot, Histogram, Bar, Line

import pandas as pd
import numpy as np


#  project_ids = [1861211] #1363324] #,1560807, 1491090, 1861211]
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


# Data handling

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


def scratch():
    '''Run the commands I keep running over and over in a terminal'''

    print('JSON incoming')
    json_all()

    print('Building dfs')
    global dfs
    dfs = {pid: build_df(pid) for pid in projects.keys()}

#    print('Calcing weeklies')
#    global weeklies
#    weeklies = {k: calc_weekly_estimates(df) for k, df in dfs.items()}
#
#    print('Calcing normed weeklies')
#    global weeklies_norm
#    weeklies_norm = {k: calc_weekly_estimates(df, normalize=True) for k, df in dfs.items()}


def count_working_hours(s):
    '''
    Return the number of working hours between
    start and end dates assuming 8 hour working days

    Args:
        s : a Story object
    '''

    start_date = s.started_date
    end_date = s.accepted_date

    if end_date is None or start_date is None:
        return None

    time_spent_day1 = dt.datetime(start_date.year,
                                  start_date.month,
                                  start_date.day,
                                  18, 0, 0) - start_date

    time_spent_dayn = end_date - dt.datetime(end_date.year,
                                             end_date.month,
                                             end_date.day,
                                             9, 0, 0)

    hours_between = np.busday_count(start_date, end_date) - 1
    total_time = (time_spent_day1
                  + dt.timedelta(hours=int(hours_between*8))
                  + time_spent_dayn)

    return total_time.total_seconds() / 3600


# DS
def build_df(pid):
    '''Build a dataframe from a project'''

    p = projects[pid]

    data = []
    data_columns = ['sid',
                    'estimate',
                    'created_date',
                    'creator',
                    'start_date',
                    'accepted_date',
                    'duration',
                    'type',
                    'pid']

    for sid, s in p.stories.items():
        try:
            # stories moved into the project may not have a creator
            if s.creator is not None:
                creator_name = s.creator.name
            else:
                creator_name = None

            story_data = (sid,
                          s.estimate,
                          s.created_date,
                          creator_name,
                          s.started_date,
                          s.accepted_date,
                          count_working_hours(s),
                          s.story_type,
                          p.project_info['id'])
        except:
            print(s.__dict__)

        data.append(story_data)

    df = pd.DataFrame(data, columns=data_columns)
    return df


def calc_weekly_estimates(df, normalize=False):
    '''
    Return a dataframe of counts of estimate numbers of created stories by week
    '''
    df1 = df

    # Stories moved in from another project have no create activity
    df1 = df1.dropna(subset=['created_date'])
    df1.index = df1['created_date']

    data = {}

    earliest = df1['created_date'].min()
    latest = df1['created_date'].max()

    datelist = pd.date_range(earliest, freq='7D', end=latest).tolist()

    for d in datelist:
        temp_df = df1[str(d):str(d + dt.timedelta(days=7))]
        vcounts = temp_df['estimate'].value_counts(normalize=normalize)
        data[str(d)] = vcounts

    return pd.DataFrame(data).fillna(0).transpose()


# Need a clean dropna'd df to plot  with
def clean_df(pid, duration_limit=None):
    '''
    Return a dropna'd df identified by project pid.
    NOTE: This implicitly drops all non-feature stories
    '''

    if not dfs[pid].empty:
        data = dfs[pid].dropna(
            subset=['estimate', 'duration']
            ).sort_values(by='estimate')

    if duration_limit is not None:
        data = data.loc[data['duration'] < duration_limit]

    return data


def accepted_stories(pid):
    '''Return a dict of dates and story IDs of accepted stories'''

    if pid in projects.keys():
        p = projects[pid]
    else:
        return

    accepted_list = {}

    for k, s in p.stories.items():
        for d, state in s.state_changes.items():
            if state == 'accepted':
                accepted_list[d] = k

    return accepted_list


# Visualisations
def show_scatter(pid, x=None, y=None):

    if pid in projects.keys():
        df = clean_df(pid)
    else:
        return

    if not df.empty:
        output_file('./scatter.html')
        p = Scatter(df, x=x, y=y, xlabel=x, ylabel=y)
        show(p)


def show_boxplot(pid, duration_limit=None):
    '''Generate a boxplot of story points vs duration'''

    if pid in projects.keys():
        df = clean_df(pid, duration_limit)
    else:
        return

    project_name = projects[pid].project_info['name']

    if not df.empty:
        output_file("./%(pid)d_boxplot.html" % {"pid": pid})
        p = BoxPlot(df,
                    label='estimate',
                    values='duration',
                    title=project_name + ' estimated story duration',
                    color='estimate')
        show(p)


def hist_points(pid, duration_limit=None):
    '''Show a histogram of duration of stories colored by estimate'''

    if pid in projects.keys():
        p = projects[pid]
    else:
        return

    project_name = p.project_info['name']
    data = clean_df(pid, duration_limit)

    if not data.empty:
        data = data.dropna()
        output_file("./%(pid)d_hist_points.html" % {'pid': pid})
        hist = Histogram(data,
                         values='duration',
                         color='estimate',
                         bins=20,
                         legend='top_right',
                         title=project_name + ' estimated story duration',
                         ylabel='Number of stories',
                         xlabel='Working hours from Started to Accepted')
        show(hist)


def story_creators(pid):
    '''Show a line chart of stories created by person over time'''

    if pid in projects.keys():
        df = build_df(pid)
        project_name = projects[pid].project_info['name']
    else:
        return

    output_file("./%(pid)d_story_creators.html" % {"pid": pid})

    df['counter'] = 1
    df.sort_values(by='created_date')
    df.index = df['created_date']
    grouped_stories = df.groupby('creator')

    munged_df = []
    for name, group in grouped_stories:
        story_count = group.resample('W').sum()
        story_count['creator'] = name
        story_count = story_count.reset_index()
        munged_df.append(story_count)

    new_df = pd.concat(munged_df)
    new_df['counter'] = new_df['counter'].fillna(0)

    p = Line(new_df,
             x='created_date',
             y='counter',
             color='creator',
             legend='top_right',
             xlabel='Date',
             ylabel='Stories created',
             title="%(name)s stories created by date" % {'name': project_name})

    show(p)


# Storytelling
def tell_me_about(pid, duration_limit=None):
    '''Generate an overview of a project'''

    # Histogram of how long it took to deliver stories broken up by estimate
    hist_points(pid, duration_limit)

    # Boxplot of stories and durations
    show_boxplot(pid, duration_limit)

    # Stories created by person over time
    story_creators(pid)
