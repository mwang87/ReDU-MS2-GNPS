# main.py
from app import app
from models import *
import views
import views_selection
import views_pca

if __name__ == '__main__':
    Filename.create_table(True)
    Attribute.create_table(True)
    AttributeTerm.create_table(True)
    FilenameAttributeConnection.create_table(True)
    app.run(host='0.0.0.0', port=5001)
