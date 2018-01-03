# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 10:02:58 2017

@author: gribl
"""

import unittest
from namegenerator import get_forename, get_surname, get_full_name, get_gender, forenames, surnames, genders

fn_list = set().union(*[forenames[g] for g in genders])

class TestGetForename(unittest.TestCase):
	def setUp(self):
		pass

	def test_get_forename(self):

		self.assertTrue(get_forename('male') in forenames['male'])
		self.assertTrue(get_forename('female') in forenames['female'])
		self.assertTrue(get_forename(3) in fn_list)
		self.assertTrue(get_forename(None) in fn_list)
		self.assertTrue(get_forename('') in fn_list)
		self.assertTrue(get_forename('adsada') in fn_list)

class TestGetSurname(unittest.TestCase):
	def setUp(self):
		pass

	def test_get_surname(self):
		self.assertTrue(get_surname() in surnames)

class TestGetFullName(unittest.TestCase):
	def setUp(self):
		pass

	def test_get_fullname(self):
		default_name = get_full_name(None).split()
		male_name = get_full_name('male').split()
		female_name = get_full_name('female').split()

		self.assertTrue(default_name[0] in fn_list)
		self.assertTrue(default_name[1] in surnames)
		self.assertTrue(male_name[0] in forenames['male'])
		self.assertTrue(male_name[1] in surnames)
		self.assertTrue(female_name[0] in forenames['female'])
		self.assertTrue(female_name[1] in surnames)


class TestGetGender(unittest.TestCase):

	def setUp(self):
		pass

	def test_get_gender(self):
		self.assertTrue(get_gender('male') == 'male')
		self.assertTrue(get_gender('female') == 'female')
		self.assertTrue(get_gender('hghgj') in genders)
		self.assertTrue(get_gender(None) in genders)

if __name__ == '__main__':
	unittest.main()