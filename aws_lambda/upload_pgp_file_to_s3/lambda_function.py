import re, boto3
from time import time
from pgpdump import AsciiData


DYNAMODB_TABLE = 'jobs-ho600-com'
S3_LOCATION = 's3://exam.yueh-cake.com/jobs.at.ho600'

def lambda_handler(event, context):
    """
    :param event:
    :param context:
    :return:

    INFO: pgpdump has problem on parse expiration_time.
    """
    public_key_content = d.get('public_key_content', '')
    if public_key_content:
        ad = AsciiData(public_key_content)
        adps = list(ad.packets())
        pub_algorithm_type = adps[0].pub_algorithm_type.lower()
        raw_pub_algorithm = adps[0].raw_pub_algorithm
        if pub_algorithm_type != 'rsa' or raw_pub_algorithm != 1:
            raise Exception('403 Forbidden: PublicKey TypeError')
        user_name = adps[1].user_name.lower()
        if re.sub('(applicants|[ \(\)])', '', user_name):
            raise Exception('403 Forbidden: PublicKey UserNameError')
        user_email = adps[1].user_email.lower()
        dynamo = boto3.resource('dynamodb').Table(DYNAMODB_TABLE)
        response = dynamo.get_item(Key={'email': user_email,
                                        'type': 'apply-account-at-exam.yueh-cake.com'})
        item = response.get('Item', {})
        if not item:
            raise Exception('403 Forbidden: PublicKey EmailAddressDoesNotExist')
        elif (int(item['timestamp']) + 86400) < int(time()):
            raise Exception('403 Forbidden: EmailAddressExpiration')
        elif item.get('public_key_id', ''):
            raise Exception('403 Forbidden: PublicKeyAlreadyExist')


        public_key_id = adps[3].key_id[-8:].upper()
        user_directory = '%s/%s-%s' % (S3_LOCATION, user_email, public_key_id)
        #TODO: copy index.html to user_directory
        #TODO: upload 0A.asc to user_directory

        response = dynamo.update_item(Key={'email': user_email,
                                           'type': 'apply-account-at-exam.yueh-cake.com'},
                                      UpdateExpression="set public_key_id = :public_key_id",
                                      ExpressionAttributeValues={":public_key_id": public_key_id},
                                      ReturnValues="UPDATED_NEW",
                                      )


    pass



if __name__ == '__main__':
    d = {
        "email": "",
        "public_key_content": "",
        "filename": "0A.gpg",
        "encrypt_content": "",
         }
    lambda_handler(d, None)
