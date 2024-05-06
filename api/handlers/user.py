from tornado.web import authenticated

from .auth import AuthHandler
from api.encrypt_utils import  decrypt_data


class UserHandler(AuthHandler):

    @authenticated
    def get(self):
        self.set_status(200)
        self.response['email'] = decrypt_data(self.current_user['email'])
        self.response['displayName'] = decrypt_data(self.current_user['display_name'])
        self.response['full_name'] = decrypt_data(self.current_user['full_name'])
        self.response['address'] = decrypt_data(self.current_user['address'])
        self.response['dob'] = decrypt_data(self.current_user['dob'])
        self.response['phone_number'] = decrypt_data(self.current_user['phone_number'])
        self.response['disabilities'] = decrypt_data(self.current_user['disabilities'])
        self.write_json()