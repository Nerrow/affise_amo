from flask import Flask, request
from flask_cors import CORS
import requests as rq

application = Flask(__name__)
CORS(application)

with open('access_token.txt', 'r') as file:
    amo_token = file.read()


@application.route('/', methods=['GET'])
def create_contact():
    return '<h1>Affise -> amoCRM -> vk-helper -> Affise Works great!</h1>'


@application.route('/affise', methods=['POST'])
def affise():
    try:
        lead_id = request.form.get('leads[status][0][id]')
        get_amo_update_lead = rq.get(f'https://podruzhki.amocrm.ru/api/v4/leads/{lead_id}',
                                     headers={'Authorization': f'Bearer {amo_token}'})
        if get_amo_update_lead.json()['custom_fields_values'][1]['field_name'] == 'CLICKID':
            clickid = get_amo_update_lead.json()['custom_fields_values'][1]['values'][0]['value']
            conversation = rq.get(f"https://offers-podruge.affise.com/postback?clickid={clickid}")
        else:
            pass
    except KeyError as e:
        print(f"ERROR: {e}")

    return 'ok'

if __name__ == '__main__':
    application.run()
