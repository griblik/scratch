# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 14:36:12 2016

@author: ntelford
"""

import csv
import re
from datetime import date

class Project:
    def __init__(self, id=None, name='untitled', budget=0, hours={}):
        self.name = name
        self.id = id
        self.weeks = {}
        
class week():
    
    def __init__(self, wcdate, hours={}):
        self.wcdate = wcdate
        self.hours = hours

    

def read_list(file, column):
    ''' return a column from a csv as a list where the cell is not a single space '''
    result = []
    with open(file) as rolesfile:
        rolesreader = csv.DictReader(rolesfile, delimiter=',')
        for row in rolesreader:
            if row[column] != ' ' :
                result.append(row[column])
    return result
    

def read_projects():
    ''' read the projects csv file and return a Dict of proj name: Project objs'''
    file='Project hours - Projects.csv'    
    
    result = {}
    with open(file) as rolesfile:
        rolesreader = csv.DictReader(rolesfile, delimiter=',')
        for row in rolesreader:
            if row['Project'] != ' ' :
                result[row['Project']] = Project(name=row['Project'], id=row['Internal id'])
    return result
    
# read the staff roles list
roles = read_list('Project hours - roles.csv', 'Job code')

# Get a list of the current project names
projects = read_projects()

# Read the hours sheet and create weeks for each column per project
def read_hours():
    file='Project hours - project hours by role.csv'
    with open(file) as hoursfile:
        hoursreader = csv.reader(hoursfile, delimiter=',')
        hoursreader.__next__()
        
        datematch = re.compile('\d+')
        weeksrow=[]

        for wd in hoursreader.__next__():
            if datematch.findall(wd):
                print(wd)
                m, d, y = datematch.findall(wd)
                weeksrow.append(date(int(y),int(m),int(d)))
        print(weeksrow)
        
        currentproject = ''
        for row in hoursreader:
            if row[0] in projects.keys():
                currentproject=projects[row[0]]
                continue
            

                
read_hours()
