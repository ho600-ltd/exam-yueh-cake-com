from __future__ import print_function

import boto3
import time
import re

from hashlib import md5
from random import random

DYNAMODB_TABLE = 'jobs-ho600-com'


def lambda_handler(event, context):
    '''
    '''
    dynamo = boto3.resource('dynamodb').Table(DYNAMODB_TABLE)
    type = event.get('type', '')

    if type in ('employee', 'non-ROC'):
        unique_email = re.sub('\+[^@]+@', '@', event['email'])
        name, domain = unique_email.split('@', 1)
        unique_email = '%s@%s' % (name.replace('.', ''), domain)
        email = event['email']
        message = ''
    elif type == 'apply-account-at-exam.yueh-cake.com':
        unique_email = '%s@exam.yueh-cake.com' % md5(str(random())).hexdigest().lower()
        email = unique_email
        message = unique_email
    else:
        raise Exception('403 Forbidden: no type')

    response = dynamo.get_item(
        Key={'email': unique_email, 'type': type})
    if response.get('Item', {}):
        return {'status': 200,
                'message': '%s was exist' % event.get('email', '__none__')}

    create_function = lambda x: dynamo.put_item(Item={"timestamp": int(time.time()),
                                                      "email": unique_email,
                                                      "type": type,
                                                      "pathname": x['pathname'],
                                                      "original_email": email})

    try:
        HTTPStatusCode = create_function(event)['ResponseMetadata'][
            'HTTPStatusCode']
    except:
        HTTPStatusCode = 403

    if HTTPStatusCode == 200:
        return {'status': 200, 'message': message}
    else:
        raise Exception('403 Forbidden: %s' % event.get('email', '__none__'))