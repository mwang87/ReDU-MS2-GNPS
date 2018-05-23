# main.py
from app import app
from models import *
import views

if __name__ == '__main__':
    Filename.create_table(True)
    Attribute.create_table(True)
    AttributeTerm.create_table(True)
    FilenameAttributeConnection.create_table(True)
    app.run()
