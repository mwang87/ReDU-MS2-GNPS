# models.py
import datetime

from peewee import *

from app import db

class Filename(Model):
    filepath = TextField(primary_key=True)

    class Meta:
        database = db

class Attribute(Model):
    categoryname = TextField(primary_key=True)

    class Meta:
        database = db

class AttributeTerm(Model):
    term = TextField(primary_key=True)

    class Meta:
        database = db

class FilenameAttributeConnection(Model):
    filename = ForeignKeyField(Filename)
    attribute = ForeignKeyField(Attribute)
    attributeterm = ForeignKeyField(AttributeTerm)

    class Meta:
        database = db
        #@primary_key = False
        primary_key = CompositeKey('filename', 'attribute', 'attributeterm')
