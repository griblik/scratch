# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 14:36:12 2016

@author: ntelford
"""

import csv
import re
from datetime import date

class Project:
    def __init__(self, id=None, name='untitled', budget=0, weeks=[]):
        self.name = name
        self.id = id
        self.weeks = weeks
        
class Week():
    
    def __init__(self, wcdate, hours={}):
        self.wcdate = wcdate
        self.hours = hours
        
    def set_hours(self, role, hours):
        self.hours[role] = hours
        
    def get_date(self):
        return self.wcdate

    

def read_roles():
    ''' return a column from a csv as a list where the cell is not a single space '''

    file = 'Project hours - roles.csv'
    column = 'Job code'

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
        weekdates=[]
        
        # Read the week dates from the head of the table
        for wd in hoursreader.__next__():
            # only store columns containing dates - first cell doesn't
            if datematch.findall(wd):
                m, d, y = datematch.findall(wd)
                weekdates.append(Week(wcdate=date(int(y),int(m),int(d))))
        
        #Set up the week objects for each project
        for p in projects.values():
            p.weeks = [Week(wcdate=weekdates[i].wcdate) for i in range(0,len(weekdates))]
        
        # Clean up the data
        hoursreader = list(hoursreader)
        hoursreader = [row[:-1] for row in hoursreader][:-2]    # remove the totals column and 2 footer rows
        for row in hoursreader:
            row[0] = row[0].strip()     # Strip the leading spaces from role title


        # Sheet lists projects and roles. Read the role hours into each project


        for row in hoursreader:
            '''
            For each row in the csv:
                read the row
                If it's a proj, change proj
                If it's a role, loop through the row and add role:hours to the project week
            '''
        
            if row[0] in projects.keys():                
                currentproject = projects[row[0]] # switch projects
                continue
            
            # If it's not a project, and it's not a role, we don't want it
            elif row[0] not in roles:
                continue
            
            print(currentproject.name)

            # Add rolename:hours to each week. 
            for i in range(0, len(row)-1):
                print('Setting ', currentproject.name, ' week ',currentproject.weeks[i].get_date(), ' role: ', row[0], ' hours: ',round(float(row[i+1]), 2))
                currentproject.weeks[i].set_hours(role=row[0], hours=round(float(row[i+1]), 2))


# read the staff roles list
roles = read_roles()

# Get a list of the current project names
projects = read_projects()

# Assign the hours submitted to each project
read_hours()

#for proj in projects:
#    print(proj)
#    print(projects[proj].weeks[-4].hours)
