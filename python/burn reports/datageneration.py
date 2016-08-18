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
        
class Week():
    
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
    '''Read the hours per project sheet and set the hours attribute of each 
        project to a list of week containing the hours'''
    file='Project hours - project hours by role.csv'
    
    # read the file
    with open(file) as hoursfile:
        hoursreader = csv.reader(hoursfile, delimiter=',')
        hoursreader.__next__()
        
        
        # Extract the weeks covered  by the sheet
        datematch = re.compile('\d+')
        weeks=[]
        
        # Read the week dates from the head of the table
        for wd in hoursreader.__next__():
            # only store columns containing dates - first cell doesn't
            if datematch.findall(wd):
                m, d, y = datematch.findall(wd)
                weeks.append(Week(wcdate=date(int(y),int(m),int(d))))
        print(weeks[102].wcdate)
        
        # Sheet lists projects and roles. Read the role hours into each project
        currentproject = ''
        for row in hoursreader:
            
            # next project in the sheet
            if row[0] in projects.keys():
                currentproject=projects[row[0]]
                continue
            
            # If it's not a project, and it's not a role, we don't want it
            if row[0] not in roles:
                continue
            
            # Determine the role
            role = row[0].strip()
#            print(len(row),  ' - ', len(weeks))
            # Add the hours for that role to each week
            for i in range(0, len(weeks)):
                print(row[0], ' ==== ', currentproject.name)
                weeks[i].hours[role] = round(float(row[i+1]), 2)

        print(weeks[4].hours)
   
read_hours()


