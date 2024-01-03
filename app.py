from flask import Flask, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# Get the values of environment variables for connecting to the database
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_uri = os.environ.get('DB_URI')

app = Flask(__name__, template_folder='templates')

# Use variable values in Flask configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_uri}/your_database'


db = SQLAlchemy(app)


# Model for storing contacts
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

# Route for serving static frontend files


@app.route('/frontend/<path:path>')
def serve_frontend(path):
    return send_from_directory('path/to/your/frontend', path)

# Route for home page


@app.route('/')
def index():
    return send_from_directory('path/to/your/frontend', 'index.html')

# Route for contact page


@app.route('/contacts')
def contacts():
    contacts = Contact.query.all()
    return render_template('contacts.html', contacts=contacts)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
