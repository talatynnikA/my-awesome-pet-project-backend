from flask import Flask, send_from_directory, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import os
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_uri = os.environ.get('DB_URI')
print(f"db_username: {db_username}")
print(f"db_password: {db_password}")
print(f"db_uri: {db_uri}")

if None in (db_username, db_password, db_uri):
    raise ValueError("One or more of the database connection parameters are not set.")

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@localhost:5432/{db_uri}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(100), nullable=False, default='textmsg is not set')

def get_or_create_contact(name, email, message):
    contact = Contact.query.filter_by(name=name, email=email).first()
    if not contact:
        contact = Contact(name=name, email=email, message=message)
        db.session.add(contact)
        db.session.commit()
    return contact
class ContactResource(Resource):
    def get(self):
        contacts = Contact.query.all()
        contact_list = [{"id": contact.id, "name": contact.name, "email": contact.email} for contact in contacts]
        return jsonify(contact_list)

api.add_resource(ContactResource, '/api/contacts')

@app.route('/')
def index():
    # new_contact = Contact(name='John Doe', email='john@example.com')
    # db.session.add(new_contact)
    # db.session.commit()
    #return send_from_directory('frontend', 'index.html')
    return {
        'Hello': ['My name is', 'Artyom Talatynnik!',
                  'This is my demo project',
                  'Welcome!'
                  ],
        'ENV': 'test'
    }

@app.route('/contacts')
def contacts():
    return send_from_directory('frontend', 'contacts.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
