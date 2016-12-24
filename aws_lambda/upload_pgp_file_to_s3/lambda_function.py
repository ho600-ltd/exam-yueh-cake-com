import re, boto3, json
from time import time
from datetime import datetime
from pgpdump import AsciiData


DYNAMODB_TABLE = 'jobs-ho600-com'
S3_BUCKET = 'exam.yueh-cake.com'
S3_LOCATION = 'jobs.at.ho600'
PUBLIC_KEY_ID = '991028D6'

def lambda_handler(event, context):
    """
    :param event:
    :param context:
    :return:

    INFO: pgpdump has problem on parse expiration_time.
    """
    public_key_content = event.get('public_key_content', '')
    if public_key_content:
        if event['filename'] != '0A.asc':
            raise Exception('403 Forbidden: FilenameError')
        ad = AsciiData(public_key_content)
        adps = list(ad.packets())
        pub_algorithm_type = adps[0].pub_algorithm_type.lower()
        raw_pub_algorithm = adps[0].raw_pub_algorithm
        user_name = adps[1].user_name.lower()
        user_email = adps[1].user_email.lower()
        public_key_file_key_id = adps[3].key_id[-8:].upper()

        if pub_algorithm_type != 'rsa' or raw_pub_algorithm != 1:
            raise Exception('403 Forbidden: PublicKey TypeError')
        if re.sub('(applicants|[ \(\)])', '', user_name):
            raise Exception('403 Forbidden: PublicKey UserNameError')

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

        encrypt_content = event['encrypt_content']
        encrypt_file_key_id_list = []
        for pkeskp in list(AsciiData(encrypt_content).packets()):
            encrypt_file_key_id = getattr(pkeskp, 'key_id', '')[-8:].upper()
            if encrypt_file_key_id: encrypt_file_key_id_list.append(encrypt_file_key_id)
        if len(encrypt_file_key_id_list) != 2:
            raise Exception('403 Forbidden: PublicKeyCountError')
        elif PUBLIC_KEY_ID not in encrypt_file_key_id_list or public_key_file_key_id not in encrypt_file_key_id_list:
            raise Exception('403 Forbidden: PublicKeyUsageError')

        user_directory = '%s/%s-%s' % (S3_LOCATION, user_email, public_key_file_key_id)
        index_html = re.sub('<div id="build_version">.*</div>',
                            '<div id="create_time">Create Time at %s</div>'%datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S+UTC'),
                            open('index.html', 'r').read())

        client = boto3.client('s3')
        response = client.put_object(
            ACL='public-read',
            Body=index_html,
            Bucket=S3_BUCKET,
            ContentType='text/html',
            Key='%s/index.html' % user_directory,
            StorageClass='STANDARD',
        )
        response = client.put_object(
            ACL='public-read',
            Body=encrypt_content,
            Bucket=S3_BUCKET,
            ContentType='text/plain',
            Key='%s/0A.asc' % user_directory,
            StorageClass='STANDARD',
        )

        response = dynamo.update_item(Key={'email': user_email,
                                           'type': 'apply-account-at-exam.yueh-cake.com'},
                                      UpdateExpression="set public_key_id = :public_key_id",
                                      ExpressionAttributeValues={":public_key_id":
                                                                     public_key_file_key_id},
                                      ReturnValues="UPDATED_NEW",
                                      )
        return {'status': 200, 'message': '/' + user_directory}


    pass



if __name__ == '__main__':
    d = {
        "public_key_content": open('3049DCE8.pkey.asc', 'r').read(),
        "filename": "0A.asc",
        "encrypt_content": open('id.txt.asc', 'r').read(),
         }
    print json.dumps(d)
    lambda_handler(d, None)
