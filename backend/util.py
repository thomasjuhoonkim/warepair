from sys import pycache_prefix
import psycopg2
import requests
import json
from flask import request
from backend.config import config


def get_db_connection():
    # conn = psycopg2.connect(host='localhost',
    #                         database='flask_db',
    #                         user=os.environ['DB_USERNAME'],
    #                         password=os.environ['DB_PASSWORD'])
    params = config()
    return psycopg2.connect(**params)

    return conn


def get_filtered_ticks(origin, destination, radius):
    print(origin)
    print(destination)
    print(radius)
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key=AIzaSyCi4Z6r3IAxS0ywrRniNwvzUFreM7poFyk'
    res = requests.get(url)
    if res.status_code == 200 and res.json()['rows'][0]['elements'][0]['status'] != 'NOT_FOUND':
        dist = float(res.json()['rows'][0]['elements']
                     [0]['distance']['text'].replace(" km", ""))
        print(dist)
        if dist <= float(radius):
            return True
    return False

# sends a email using emailjs


def send_email(receiver_email, contractor_name, template):
    headers = {'Content-Type': 'application/json'}
    data = {
        'service_id': 'service_yu6d39t',
        'template_id': 'template_fo9h03c',
        'user_id': 'nbO4c5EfFaBq5_cGS',
        'accessToken': 'pE9VdWkPfvMo0m9NmFHLH',
        'template_params': {
            'receiver_email': receiver_email,
            'contractor_name': contractor_name,
            'template': template
        }
    }
    data = json.dumps(data)
    return requests.post('https://api.emailjs.com/api/v1.0/email/send', data=data, headers=headers)


def get_contractors():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT email, location, radius FROM users WHERE is_contractor = TRUE')
    conn.commit()
    contractors = cur.fetchall()
    cur.close()
    conn.close()
    return contractors


def filter_for_relevant_request_emails(help_request, contractors):
    help_request = {
        "title": help_request["title"],
        "location": help_request["location"],
        "description": help_request["description"],
        "contact_info": help_request["contact_info"],
        "compensation": help_request["compensation"]
    }

    ret = dict()

    for contractor in contractors:
        if get_filtered_ticks(contractor[1], help_request["location"], contractor[2]):
            help_request["contractor_name"] = contractor["first_name"]
            ret[contractor["email"]] = help_request

    return ret


def create_email_template(i, help_requests):
    template = """
        A new job has appeared in your vicinity! The job is titled {} and is located at {}. The user's request 
        is "{}" and will provide a compensation of {}. If you're interested please contact: {}.
    """.format(help_requests["title"], help_requests["location"], help_requests["description"], help_requests["contact_info"], help_requests["compensation"])

    return template


def send_emails(emails_to_be_sent):
    for i, email in enumerate(emails_to_be_sent):
        template = create_email_template(i+1, emails_to_be_sent[email])
        print(template)
        send_email(email, emails_to_be_sent[email]
                   ["contractor_name"], template)
