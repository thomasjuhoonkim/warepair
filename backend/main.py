from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
import uuid
from backend.util import get_db_connection, get_filtered_ticks
from backend.emailjs import trigger_email_creation
from flask_cors import CORS, cross_origin
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="google.com")

api = Flask(__name__)
api.config['SECRET_KEY'] = 'secret'
psycopg2.extras.register_uuid()
CORS(api)

session = {}


@api.route('/register', methods=['POST'])
def register():
    conn = get_db_connection()
    cur = conn.cursor()

    user_firstname = request.form["firstname"]
    user_lastname = request.form["lastname"]
    user_password = request.form["password"]
    user_email = request.form["email"]
    user_unit = request.form["unit"]
    user_street = request.form["street"]
    user_city = request.form["city"]
    user_country = request.form["country"]
    user_is_contractor = request.form["is_contractor"]
    user_radius = request.form["radius"]

    # If user misses input field.
    if not (user_firstname and user_lastname and user_password and user_email and user_unit and user_street and user_city and user_country):
        cur.close()
        conn.close()
        return 'Missing input field'

    # Generate UUID
    user_uuid = uuid.uuid4()

    # If user already exists.
    cur.execute(f"SELECT * FROM users WHERE user_id = '{user_uuid}'")
    rows = cur.fetchall()
    if rows:
        cur.close()
        conn.close()
        return 'User already exists'

    # Register user
    cur.execute(
        "INSERT INTO users (user_id, first_name, last_name, email, password, location, is_contractor, radius) VALUES " +
        f"('{user_uuid}', '{user_firstname}', '{user_lastname}', '{user_email}', '{user_password}', '{user_unit}, {user_street}, {user_city}, {user_country}', {user_is_contractor}, {user_radius})")

    conn.commit()
    session["user_id"] = user_uuid

    cur.close()
    conn.close()
    return str(session["user_id"]) + ' registered'


@api.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    request_json = request.json
    email = request_json['email']
    password = request_json['password']

    print(email, password)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'")
    rows = cur.fetchall()

    if not rows:
        cur.close()
        conn.close()
        return 'Email and password do not match'

    session["user_id"] = rows[0][0]
    return 'Logged in'


@api.route('/test', methods=['GET'])
def get_db_values():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS users;')
    cur.execute('CREATE TABLE users (user_id varchar (100) PRIMARY KEY NOT NULL,'
                'first_name varchar (50) NOT NULL,'
                'last_name varchar (50) NOT NULL,'
                'email varchar (50) NOT NULL,'
                'password varchar (50) NOT NULL,'
                'location varchar (100)',
                'is_contractor BOOLEAN NOT NULL,'
                )
    cur.execute('DROP TABLE IF EXISTS request;')
    cur.execute('CREATE TABLE request (request_id varchar (100) PRIMARY KEY NOT NULL,',
                'user_id varchar (50) NOT NULL,',
                'title varchar (50) NOT NULL,'
                'description varchar (250) NOT NULL,'
                'location varchar (100) NOT NULL,'
                'contact_info varchar (100) NOT NULL,'
                'compensation varchar (50) NOT NULL,'
                'is_complete BOOLEAN NOT NULL,'
                )

    tables = cur.fetchall()
    cur.close()
    conn.close()
    return tables


@api.route('/logout', methods=['POST'])
def logout():
    if 'user_id' in session:
        temp = session['user_id']
        session.pop('user_id', None)
        return str(temp) + ' logged out'
    else:
        return 'No user logged in'

# @api.route('/edit-profile', methods=["PATCH"])
# def edit_profile():
#     update_profile = request.get_json()

#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         'UPDATE users SET firstname=%s, lastname=%s, password=%s, email=%s, unit=%s, street=%s, city=%s, country=%s WHERE userid == %s',
#         (
#             update_profile.user_uuid,
#             update_profile.user_firstname,
#             update_profile.user_lastname,
#             update_profile.user_password,
#             update_profile.user_email,
#             update_profile.user_unit,
#             update_profile.user_street,
#             update_profile.user_city,
#             update_profile.user_country
#         )
#     )
#     users = cur.fetchall()
#     cur.close()
#     conn.close()
#     return users

# @api.route('/test', methods=['GET'])
# def get_db_values():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute('DROP TABLE IF EXISTS users;')
#     cur.execute('CREATE TABLE users (user_id (uuid) PRIMARY KEY NOT NULL,'
#                                     'first_name varchar (50) NOT NULL,'
#                                     'last_name varchar (50) NOT NULL,'
#                                     'email varchar (50) NOT NULL,'
#                                     'password varchar (50) NOT NULL,'
#                                     'location varchar (100)',
#                                     'is_contractor BOOLEAN NOT NULL,',
#                                     'radius integer);'
#     )
#     cur.execute('DROP TABLE IF EXISTS requests;')
#     cur.execute('CREATE TABLE requests (request_id (uuid) PRIMARY KEY NOT NULL,',
#                                     'user_id varchar (50) NOT NULL,',
#                                     'title varchar (50) NOT NULL,'
#                                     'request_description varchar (50) NOT NULL,'
#                                     'location varchar (100) NOT NULL,'
#                                     'contact_info varchar (100) NOT NULL,'
#                                     'compensation varchar (50) NOT NULL,'
#                                     'is_complete BOOLEAN NOT NULL);'
#     )

#     tables = cur.fetchall()
#     cur.close()
#     conn.close()
#     return tables


@api.route('/helpRequests', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def handle_help_requests():
    conn = get_db_connection()
    cur = conn.cursor()

    print("session", session.get("user_id", 0))

    # get all help requests
    if request.method == 'GET':
        cur.execute(
            """SELECT * FROM requests WHERE is_complete = false AND user_id = %s :: VARCHAR;""", [session["user_id"]])
        help_requests = cur.fetchall()
        cur.close()
        conn.close()
        print('request tings mahn', help_requests)
        return jsonify(help_requests)

    # create a new help request
    elif request.method == 'POST':
        request_id = uuid.uuid4()
        title = request.form["title"]
        description = request.form["request_description"]
        location = request.form["location"]
        lng = str(geolocator.geocode(location).longitude)
        lat = str(geolocator.geocode(location).latitude)
        contact_info = request.form["contact_info"]
        compensation = request.form["compensation"]
        user_id = session["user_id"]

        cur.execute("""INSERT INTO requests (request_id, title, request_description, location, lng, lat, contact_info, compensation, user_id, is_complete)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (request_id, title, description, location, lng,
                     lat, contact_info, compensation, user_id, False)
                    )
        trigger_email_creation({
            "request_id": request_id,
            "title": title,
            "description": description,
            "location": location,
            "contact_info": contact_info,
            "compensation": compensation,
            "user_id": user_id
        })
        conn.commit()
        cur.close()
        conn.close()
        return f'Request {request_id} created'

    # patch a help request
    elif request.method == 'PATCH':
        request_id = request.form.get("request_id")
        cur.execute(
            'UPDATE requests SET is_complete == TRUE WHERE request_id = %s', (request_id))

        conn.commit()
        cur.close()
        conn.close()
        return f'Request {request_id} is set to completed'


@api.route('/userCenter', methods=['GET'])
def userCenter():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE user_id = '{session['user_id']}'")
    ret = dict()
    ret["lat"] = geolocator.geocode(
        cur.fetchall()[0][5].replace(",", "")).latitude
    ret["lng"] = geolocator.geocode(
        cur.fetchall()[0][5].replace(",", "")).longitude
    cur.close()
    conn.close()
    return jsonify(ret)
