import logging
import os

import requests
from flask import Flask, Response, request

from config import configure_logger

app = Flask(__name__)
configure_logger('ussd')
logger = logging.getLogger(__name__)


# *502*148
@app.route('/ussd_service')
def ussd_service():
    msisdn = request.args.get('msisdn')
    sessionId = request.args.get('sessionid') or ""
    request_type = request.args.get('type')
    ussdString = request.args.get('request')
    logger.info(request.args)

    if str(request_type) not in ['1', '2']:
        response_type = ""
        ussd_response = ""
    else:
        json_body = {
            'msisdn': msisdn,
            'sessionId': sessionId,
            'serviceCode': '502*148',
            'ussdString': ussdString
        }
        ussd_request = requests.post(os.getenv('USSD_ENDPOINT'), json=json_body, verify=False)
        ussd_response = ussd_request.text

        if ussd_response.upper().startswith('CON'):
            response_type = 2
        else:
            response_type = 3
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Msg xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:noNamespaceSchemaLocation="ussd.xsd">
    <msg>
        <sessionid>{sessionId}</sessionid>
        <response type=”{response_type}”>{ussd_response[3:]}</response>
    </msg>
</Msg>
    """
    logger.info(xml_response)
    return Response(xml_response, mimetype='text/xml')
