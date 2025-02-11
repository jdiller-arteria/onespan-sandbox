import requests
import json
import base64
from configparser import ConfigParser
from debugrequests import debug_requests_on

class Client(object):

    def __init__(self):
        cp = ConfigParser()
        cp.read('credentials.ini')
        #TODO: fail nicely if the config file is missing
        self._api_key = cp.get('onespan', 'api_key')
        self._client_id = cp.get('onespan', 'client_id')
        self._base_url = 'https://sandbox.esignlive.com/api'

    def create_package(self, first_name, last_name, email, doc, questions=[], sms_verification=None):
        # build up a dict that will be sent as json to onespan
        # to create a package
        signer = {'email': email,
                  'firstName': first_name,
                  'lastName': last_name,
                  'company': 'Acme Inc.'}
        # we can require questions or sms verification or neither but not both
        if questions:
            signer['auth'] = {
                'scheme': 'CHALLENGE',
                'challenges' : questions}
        elif sms_verification:
            signer['auth'] = {
                'scheme': 'SMS',
                'challenges' :[
                    {
                    'question': sms_verification,
                     'answer': None
                    }
                ]
            }

        #this is where the signing box will go
        #in a real document you'd want to calculate it based on the document
        field = {'page':0,
                 'top': 100,
                 'subtype':'FULLNAME',
                 'height': 50,
                 'left': 100,
                 'width': 200,
                 'type': 'SIGNATURE'
                }

        #the onespan docs say to send the docs themselves as a multipart request but
        #the swagger says to send it as base64 encoded in the json
        #I couldn't get the form data to work so I'm sending it as base64
        #which works just fine
        documents = {'approvals': [{'role': 'Role1', 'fields':[field]}],
                     'name':doc.filename,
                     'base64Content': base64.b64encode(doc.stream.read()).decode('utf-8'),
                    }

        roles = [{'id': 'Role1', 'signers': [signer]}]
        package = {'roles':roles, 'documents':[documents]}
        package['name'] = 'Sandbox Package'
        package['type'] = 'PACKAGE'
        package['emailMessage'] = 'Please sign this document'
        package['status'] = 'SENT'
        package['language'] = 'en'
        package['description'] = 'This is a test package'
        package['autocomplete'] = True

        print (json.dumps(package, indent=4))
        #send the package
        #uncomment the next line to see the raw http request and response in the
        #debug console
        #debug_requests_on()
        req = requests.post(self._base_url + '/packages',
                               headers={'Authorization': 'Basic ' + self._api_key,
                                        'Content-Type': 'application/json',
                                        'Accept': 'application/json'},
                               data=json.dumps(package))
        return req

    def get_signing_url(self, package_id):
        req = requests.get(self._base_url + '/packages/' + package_id + '/roles/role1/signingUrl/',
                           headers={'Authorization': 'Basic ' + self._api_key,
                                    'Accept': 'application/json'})
        return req

