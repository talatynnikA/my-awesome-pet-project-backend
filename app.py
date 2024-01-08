from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from collections import OrderedDict
from flask_migrate import Migrate



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
migrate = Migrate(app, db)
api = Api(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(100), nullable=False, default='textmsg is not set')

class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    linkedin = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(50))
    github = db.Column(db.String(100))

class AboutMe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)

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
    db.create_all()
    about_me_data = [
        {'section': 'Hello', 'content': 'My name is\nArtyom Talatynnik!\nThis is my demo project\nWelcome!'},
        {'section': 'Skills', 'content': 'DevOps Technologies: Kubernetes, GitLab, Terraform, AWS\nOperating Systems: Linux (Ubuntu, CentOS)\nProgramming Languages: C, C++, C#, Python\nWeb Development: HTML, HTML5, JavaScript (JS), jQuery\nDatabases: SQL (MySQL, PostgreSQL, MSSQL, Oracle)\nVersion Control: Git, GitLab\nCI/CD: Gitlab CI, Jenkins\n3D Modeling and Design: Unity, 3ds Max'},
        {'section': 'Education', 'content': "BELARUSIAN STATE TECHNOLOGICAL UNIVERSITY\nFaculty of Information Technology - 2019-2023\nBachelor's Degree in Information Technology"},
        {'section': 'Experience', 'content': "2021 - 2022 | System Administrator | Belarussian State Technological University\nSet up a network for windows computers to transfer files over FTP protocol and to use RDP connection. Ensuring data security and backup. Manage and record lessons for a variety of IT topics: Cyber Security, Cryptography, Unity Engine, CSS, HTML, JavaScript. Use git for VCS in Adobe Premiere projects, Install and manage OS Windows for video production.\n2023 Jul – Present Time | Junior DevOps | Onesoil\nManaging Gitlab CI Pipelines, Setting up Cloudfront Distributions with IaC (Terraform, Terragrunt) and other infrastructure for them, managing Kubernetes cluster, Working with docker images in AWS ECR, creating AWS CloudWatch alarms and other AWS services."},
        {'section': 'About me', 'content': '1.5+ years of experience in IT. Self-driven and results-oriented.\nRecently graduated from Belarusian State Technological University with a degree in Information Technology where started my career as a System Administrator.\nCurrently serving as a DevOps Intern at Onesoil, where I apply my knowledge and skills in optimizing Software Development processes and Cloud Automation.\nEager to contribute my expertise and continue learning in a dynamic DevOps environment.\nWell-versed in technologies such as Kubernetes, GitLab, Terraform, AWS, and Linux.'},
    ]

    for data in about_me_data:
        about_me_entry = AboutMe.query.filter_by(section=data['section']).first()
        if not about_me_entry:
            about_me_entry = AboutMe(section=data['section'], content=data['content'])
            db.session.add(about_me_entry)
            db.session.commit()

    if not ContactInfo.query.first():
        contact_info = ContactInfo(
            linkedin='https://www.linkedin.com/in/artyom-talatynnik/',
            phone='+48572072828',
            email='artsyomtalatynnik@gmail.com',
            github='https://github.com/talatynnikA'
        )
        db.session.add(contact_info)
        db.session.commit()


@app.route('/')
def index():
    init_data()  # data init
    contacts = Contact.query.all()
    contact_list = [{"id": contact.id, "name": contact.name, "email": contact.email} for contact in contacts]

    # request data from table AboutMe
    about_me_data = AboutMe.query.all()
    about_me_dict = {entry.section: entry.content for entry in about_me_data}

    # insert data from table AboutMe to response_data
    response_data = OrderedDict([
        ('Hello', about_me_dict.get('Hello', [])),
        ('Skills', about_me_dict.get('Skills', [])),
        ('Education', about_me_dict.get('Education', '')),
        ('Experience', about_me_dict.get('Experience', [])),
        ('About me', about_me_dict.get('About me', [])),
        ('Contacts', contact_list),
    ])

    return jsonify(response_data)


@app.route('/contacts')
def contacts():
    init_data()  # data init

    contact_info = ContactInfo.query.first()

    response_data = {
        'My contacts list': {
            'LinkedIn': contact_info.linkedin,
            'Phone': contact_info.phone,
            'Email': contact_info.email,
            'GitHub': contact_info.github,
        },
    }

    return jsonify(response_data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
