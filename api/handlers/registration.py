from json import dumps
from logging import info
from tornado.escape import json_decode, utf8
from tornado.gen import coroutine

from .base import BaseHandler
from api.encrypt_utils import encrypt_data, hash_password

class RegistrationHandler(BaseHandler):
# Data collected to be posted
    @coroutine
    def post(self):
        try:
            body = json_decode(self.request.body)
            email = body['email'].lower().strip()
            if not isinstance(email, str):
                raise Exception()
            password = body['password']
            if not isinstance(password, str):
                raise Exception()
            password_hash = hash_password(password)
            display_name = body.get('displayName')
            if display_name is None:
                display_name = email
            if not isinstance(display_name, str):
                raise Exception()
            full_name = body.get('full_name')
            # if not isinstance(full_name, str):
            #     raise Exception()
            address = body.get('address')
            # if not isinstance(address, str):
            #     raise Exception()
            dob = body.get('dob')
            # if not isinstance(dob, str):
            #      raise Exception()
            phone_number = body.get('phone_number')
            # if not isinstance(phone_number, str):
            #     raise Exception()
            disabilities = body.get('disabilities')
            # if not isinstance(disabilities, str):
            #     raise Exception()
            print("Data Entered: ", email, password, display_name, full_name, address, dob, phone_number, disabilities)

        except Exception as e:
            self.send_error(400, message='You must provide an email address, password and display name!')
            return
# Checking data requirements
        if not email:
            self.send_error(400, message='The email address is invalid!')
            return

        if not password:
            self.send_error(400, message='The password is invalid!')
            return

        if not display_name:
            self.send_error(400, message='The display name is invalid!')
            return
        
        if not full_name:
            self.send_error(400, message='Full Name not provided or not valid')
            return
        
        if not address:
            self.send_error(400, message='Address not provided or not valid')
            return
        
        if not dob:
            self.send_error(400, message='Date of Birth not provided or not valid')
            return
        
        if not phone_number:
            self.send_error(400, message='Phone Number not provided or not valid')
            return
        
        if not disabilities:
            self.send_error(400, message='Disability Info not provided.')
            return
        
# checking if email address exist in DB
        user = yield self.db.users.find_one({
          'email': encrypt_data(email)
        }, {})

        if user is not None:
            self.send_error(409, message='A user with the given email address already exists!')
            return
# Data to be sent to DB
        yield self.db.users.insert_one({
            'email': encrypt_data(email),
            'password': password_hash,
            'displayName': encrypt_data(display_name),
            'full_name': encrypt_data(full_name),
            'address': encrypt_data(address),
            'dob': encrypt_data(dob),
            'phone_number': encrypt_data(phone_number),
            'disabilities': encrypt_data(disabilities)
        })
# Data reported back
        self.set_status(200)
        self.response['email'] = email
        self.response['displayName'] = display_name
        self.response['full_name'] = full_name
        self.response['address'] = address
        self.response['dob'] = dob
        self.response['phone_number'] = phone_number
        self.response['disabilities'] = disabilities

        self.write_json()
