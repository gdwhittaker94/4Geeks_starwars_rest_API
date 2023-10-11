import os
from flask_admin import Admin
from models import db, Users, Characters, Planets, Vehicles, Favorite_Characters, Favorite_Planets, Favorite_Vehicles
from flask_admin.contrib.sqla import ModelView  # ModelView generates the GUI for our database 

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here (from models.py), for example this is how we add the 'User' model to the admin
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Characters, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Vehicles, db.session))
    admin.add_view(ModelView(Favorite_Characters, db.session))
    admin.add_view(ModelView(Favorite_Planets, db.session))
    admin.add_view(ModelView(Favorite_Vehicles, db.session))


    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))