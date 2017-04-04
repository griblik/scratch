# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 15:41:47 2017

@author: ntelford
"""

import requests
from datetime import datetime


class Project(object):
    '''A Tracker project defined by project id'''

    def __init__(self, project_id):
        self.project_id = project_id
        self.project_url = "https://www.pivotaltracker.com/services/v5/projects/%(project_id)s" % {"project_id":project_id}
        self.pagination = {"offset": 0, "limit": 500}
        self.project_info = []
        self.activity = []
        self.stories = {}
        self.people = {}
        self.state_timeline = []
        self.deleted = False

    #  Retrieving data from the API
    def _get_project_info(self, api_key):
        '''Get the project info from the API based on the project ID'''

        r = requests.get(self.project_url, headers={"X-TrackerToken": api_key})

        if r.ok:
            self.project_info = r.json()
            print(self.project_info['name'])
        else:
            r.raise_for_status()

    def _get_activity_page(self, api_key):
        '''Request a single page of activity.'''

        activity_url = self.project_url + "/activity"

        r = requests.get(activity_url, self.pagination, headers={"X-TrackerToken": api_key})
        if(r.ok):
            return r
        else:
            r.raise_for_status()

    def _get_paginated_activity(self, api_key):
        '''
        Request pages of activity until no results are returned and store
        the responses in the project activity attribute
        '''

        have_results = True
        while(have_results):
            current_batch = self._get_activity_page(api_key).json()
            self.activity.extend(current_batch)

            self.pagination['offset'] = self.pagination['offset'] + 500
            print("Current offset: %(offset)d" % {'offset': self.pagination['offset']})

            have_results = len(current_batch) > 0

        # Tracker API provides activity latest first
        self.activity = self.activity[::-1]

    #  Handle data from the activity API
    def _parse_stories(self):
        '''
        Parse the activity JSON into story objects.
        Currently only looking for story create, updates and deletes.
        '''

        for action in self.activity:

            handled = ['story_create_activity',
                       'story_update_activity',
                       'story_delete_activity',
                       'story_move_into_project_and_prioritize_activity',
                       'story_move_into_project_activity',
                       'model_import_activity']

            if action['kind'] not in handled:
                continue

            for action_resources in action['primary_resources']:
                sid = action_resources['id']

                # Create the story object if it doesn't already exist.
                if sid not in self.stories.keys():
                    self.stories[sid] = Story(sid,
                                              action_resources['story_type'],
                                              action_resources['name'],
                                              action_resources['kind'])

            current_story = self.stories[sid]

            if action['kind'] == 'story_create_activity':
                self._handle_create_activity(action)

            if action['kind'] == 'story_update_activity':
                self._handle_update_activity(action)

            if action['kind'] == 'story_delete_activity':
                self._handle_delete_activity(action)

            if action['kind'] in ['story_move_into_project_and_prioritize_activity', 'story_move_into_project_activity']:
                self._handle_moved_activity(action)

            if action['kind'] == 'model_import_activity':
                self._handle_import_activity(action)

    def _handle_delete_activity(self, action):
        sid = action['primary_resources'][0]['id']
        activity_date = self._from_datestring(action['occurred_at'])
        current_story = self.stories[sid]

        current_story.deleted = True
        current_story.track_state_change(activity_date, "deleted")

    def _handle_import_activity(self, action):
        '''Create a Story from the activity and track it'''

        creator = self._get_person_by_id(action['performed_by'])

        for change in action['changes']:
            if change['kind'] == 'story':
                s = self.stories[change['id']]

                s.creator = creator
                s.created_date = self._from_datestring(action['occurred_at'])
                s.track_state_change(s.created_date, 'unscheduled')

    def _handle_moved_activity(self, action):
        '''Capture story creation from an imported story action'''

        creator = self._get_person_by_id(action['performed_by'])

        # Could be multiple stories moved
        for change in action['changes']:
            if change['kind'] == 'story':
                s = self.stories[change['id']]

                s.creator = creator
                s.created_date = self._from_datestring(action['occurred_at'])
                s.track_state_change(s.created_date, 'unscheduled')

                change_date = self._from_datestring(action['occurred_at'])
                s.track_state_change(change_date, change['new_values']['current_state'])

    def _handle_create_activity(self, action):
        '''Capture story creation info from a story_create_activity action'''
        s = self.stories[action['primary_resources'][0]['id']]

        created = self._from_datestring(action['occurred_at'])
        s.created_date = created
        s.track_state_change(created, 'unscheduled')

        s.creator = self._get_person_by_id(action['performed_by'])

    def _handle_update_activity(self, action):
        '''Handle an update activity. Currently only covering status changes'''

        s = self.stories[action['primary_resources'][0]['id']]

        for change_item in action['changes']:

            if 'new_values' not in change_item.keys():
                continue

            new_state = change_item['new_values']

            # commenting on a story is update activity with no original_value
            if change_item['kind'] != 'story':
                continue

            old_state = change_item['original_values']

            # Capture state change dates
            if 'current_state' in new_state.keys():
                if (new_state['current_state'] != old_state['current_state']):

                    # Track the state change
                    change_date = self._from_datestring(action['occurred_at'])
                    s.track_state_change(change_date, new_state['current_state'])

                    # Find first start date (might be rejected and restarted)
                    if new_state['current_state'] == 'started':
                        if s.started_date is None or s.started_date > change_date:
                            s.started_date = change_date

                    # Find last accepted date (might have been reopened)
                    if new_state['current_state'] == 'accepted':
                        s.acceptor = self._get_person_by_id(action['performed_by'])
                        if s.accepted_date is None or s.accepted_date < change_date:
                            s.accepted_date = change_date

            if 'estimate' in new_state.keys():
                s.estimate = new_state['estimate']

    def _get_person_by_id(self, person_info):

        pid = person_info['id']

        if pid not in self.people.keys():
            self.people[pid] = Person(
                person_info['name'],
                person_info['id'],
                person_info['initials'])

        return self.people[pid]

    def get_project_data(self, api_key):
        ''' Retrieve content from the API and populate the Project object '''
        try:
            self._get_project_info(api_key)
            self._get_paginated_activity(api_key)

            if self.stories == {}:
                self._parse_stories()
        except:
            raise

    def get_status_counts(self):
        '''Return a list of dicts of date, and +/- counts for each status'''
        change_list = []
        for s in self.stories.values():
            change_list = change_list + s.map_state_changes()

        return change_list

    # Utilities
    def _from_datestring(self, date_string):
        '''Return a datetime object from a Tracker datestring'''

        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')


class Story(object):
    '''A story within a tracker project'''

    def __init__(self, story_id, story_type, story_name, story_kind):
        self.story_id = story_id
        self.story_type = story_type
        self.story_name = story_name
        self.story_kind = story_kind
        self.creator = None
        self.acceptor = None

        self.created_date = None
        self.started_date = None
        self.delivered_date = None
        self.accepted_date = None
        self.state_changes = {}
        self.estimate = None
        self.deleted = False

    def track_state_change(self, date, state=None):
        self.state_changes[date] = state

    def map_state_changes(self):
        '''
        Return a list of dates for each change of states,
        e.g. +1 started, -1 unstarted
        '''
        state_counts = []
        previous_state = None

        for c in sorted(self.state_changes.keys()):
            change = self._state_change()
            change[self.state_changes[c]] = 1
            if previous_state:
                change[previous_state] = -1

            previous_state = self.state_changes[c]
            change['date'] = c
            state_counts.append(change)

        return state_counts

    def _state_change(self, accepted=0,
                      deleted=0,
                      delivered=0,
                      finished=0,
                      rejected=0,
                      started=0,
                      unscheduled=0,
                      unstarted=0):

        change = {'accepted': accepted,
                  'deleted': deleted,
                  'delivered': delivered,
                  'finished': finished,
                  'rejected': rejected,
                  'started': started,
                  'unscheduled': unscheduled,
                  'unstarted': unstarted}

        return change


class Person(object):

    def __init__(self, name, person_id, initials):
        self.name = name
        self.id = person_id
        self.initials = initials
