# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 20:38:25 2017

@author: nath
"""

from django.db import models

class DiveCentre(models.Model):
    name = models.TextField()
    
    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.TextField()
    dive_centre = models.ForeignKey(DiveCentre)
    
    def __str__(self):
        return self.name


class DiveSite(models.Model):
    name = models.TextField()
    description = models.TextField()
    lat = models.FloatField()
    long = models.FloatField()
    
    def __str__(self):
        return self.name


class Gallery(models.Model):
    pass


class Photo(models.Model):
    pass


class Course(models.Model):
    name = models.TextField()
    description = models.TextField()
    slug = models.SlugField()
    
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.TextField()
    content = models.TextField()
    slug = models.SlugField()
    
    def __str__(self):
        return self.title


class StaffMember(models.Model):
    pass


class Diver(models.Model):
    pass

