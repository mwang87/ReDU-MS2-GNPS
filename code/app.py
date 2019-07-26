# app.py
import os

from flask import Flask
from peewee import SqliteDatabase

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(APP_ROOT, './database/metadata.db')
DEBUG = False

class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    block_start_string='(%',
    block_end_string='%)',
    variable_start_string='((',
    variable_end_string='))',
    comment_start_string='(#',
    comment_end_string='#)',
  ))

app = CustomFlask(__name__)
app.config.from_object(__name__)
db = SqliteDatabase(app.config['DATABASE'], pragmas=[('journal_mode', 'wal')])

app.config['UPLOAD_FOLDER'] = './tempuploads'

try:
    os.mkdir(app.config['UPLOAD_FOLDER'])
except:
    print("Cannot Create", app.config['UPLOAD_FOLDER'])
