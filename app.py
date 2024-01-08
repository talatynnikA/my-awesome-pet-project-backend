from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from collections import OrderedDict
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

def init_data():
    # Инициализация данных при первом запуске
    contacts_data = [
        {'name': 'Artyom Talatynnik', 'email': 'artsyomtalatynnik@gmail.com', 'message': 'Hello, World!'},
    ]
    for data in contacts_data:
        get_or_create_contact(data['name'], data['email'], data['message'])

@app.route('/')
def index():
    init_data()  # Инициализация данных
    contacts = Contact.query.all()
    contact_list = [{"id": contact.id, "name": contact.name, "email": contact.email} for contact in contacts]

    response_data = OrderedDict([
        ('Hello', [
            'My name is',
            'Artyom Talatynnik!',
            'This is my demo project',
            'Welcome!',
        ]),
        ('ENV', 'test'),
        ('Skills', [
            'DevOps Technologies: Kubernetes, GitLab, Terraform, AWS',
            'Operating Systems: Linux (Ubuntu, CentOS)',
            'Programming Languages: C, C++, C#, Python',
            'Web Development: HTML, HTML5, JavaScript (JS), jQuery',
            'Databases: SQL (MySQL, PostgreSQL, MSSQL, Oracle)',
            'Version Control: Git, GitLab',
            'CI/CD: Gitlab CI, Jenkins',
            '3D Modeling and Design: Unity, 3ds Max',
        ]),
        ('Education', "BELARUSIAN STATE TECHNOLOGICAL UNIVERSITY\nFaculty of Information Technology - 2019-2023\nBachelor's Degree in Information Technology"),
        ('Experience', [
            "2021 - 2022 | System Administrator | Belarussian State Technological University\nSet up a network for windows computers to transfer files over FTP protocol and to use RDP connection. Ensuring data security and backup. Manage and record lessons for a variety of IT topics: Cyber Security, Cryptography, Unity Engine, CSS, HTML, JavaScript. Use git for VCS in Adobe Premiere projects, Install and manage OS Windows for video production.",
            "2023 Jul – Present Time | Junior DevOps | Onesoil\nManaging Gitlab CI Pipelines, Setting up Cloudfront Distributions with IaC (Terraform, Terragrunt) and other infrastructure for them, managing Kubernetes cluster, Working with docker images in AWS ECR, creating AWS CloudWatch alarms and other AWS services.",
        ]),
        ('About me', [
            '1.5+ years of experience in IT. Self-driven and results-oriented.',
            'Recently graduated from Belarusian State Technological University with a degree in Information Technology where started my career as a System Administrator.',
            'Currently serving as a DevOps Intern at Onesoil, where I apply my knowledge and skills in optimizing Software Development processes and Cloud Automation.',
            'Eager to contribute my expertise and continue learning in a dynamic DevOps environment.',
            'Well-versed in technologies such as Kubernetes, GitLab, Terraform, AWS, and Linux.',
        ]),
        ('Contacts', contact_list),
    ])

    return jsonify(response_data)

@app.route('/contacts')
def contacts():
    init_data()  # Инициализация данных
    contacts = Contact.query.all()
    contact_list = [{"id": contact.id, "name": contact.name, "email": contact.email} for contact in contacts]

    response_data = {
        'My contacts list': {
            'LinkedIn': 'https://www.linkedin.com/in/artyom-talatynnik/',
            'Phone': '+48572072828',
            'Email': 'artsyomtalatynnik@gmail.com',
            'GitHub': 'https://github.com/talatynnikA',
        },
        'Contacts': contact_list,
    }

    return jsonify(response_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
