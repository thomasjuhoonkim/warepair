import requests
import json
from backend.util import *

# help_request = {
#     "user_id": "1",
#     "title": "title1",
#     "description": "description1",
#     "location": "875, Dufferin St, Toronto, Canada",
#     "contact_info": "phone1",
#     "compensation": "comp1",
#     "is_complete": False
# }


# contractors = [
#     {
#         "first_name": "f1",
#         "last_name": "l1",
#         "email": "danielfang2001@gmail.com",
#         "password": "pw1",
#         "location": "290, Bremner Blvd, Toronto, Canada",
#         "is_contractor": True,
#         "radius": 9
#     },
#     {
#         "first_name": "f2",
#         "last_name": "l2",
#         "email": "email2@email.com",
#         "password": "pw2",
#         "location": "290, Bremner Blvd, Toronto, Canada",
#         "is_contractor": True,
#         "radius": 6
#     },
#     {
#         "first_name": "f3",
#         "last_name": "l3",
#         "email": "email3@email.com",
#         "password": "pw3",
#         "location": "290, Bremner Blvd, Toronto, Canada",
#         "is_contractor": True,
#         "radius": 7
#     },
# ]

def trigger_email_creation(help_request):
    contractors = get_contractors()

    emails_to_be_sent = filter_for_relevant_request_emails(
        help_request, contractors)
    send_emails(emails_to_be_sent)
