#/usr/bin/env python2
# -*- coding: utf-8 -*-
import re, boto3, json
from time import time
from datetime import datetime
from pgpdump import AsciiData
from random import shuffle


DYNAMODB_TABLE = 'jobs-ho600-com'
S3_BUCKET = 'exam.yueh-cake.com'
S3_LOCATION = 'jobs.at.ho600'
PUBLIC_KEY_ID = '991028D6'
PUBLIC_KEY_CONTENT = '''-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBFheeSkBCACo3s9tknTR0wHIJ20Onjpq5y50sZ/Qu9IRG7A6L+7daYVIPDI7
4YkQevfzpih6WDNrUuGAuTqHDE5085F7vMQXGtqOYOuz6/H+gRUsPnaJhm0CJirU
VeSsDYIL+CL4AvA3sHJtjAhg67VsEbaHAOnTiXs4c0lVmEPxCfklXBXzh/ekBD40
1PFFGshtfcyASoT+BBNdN2UZ5re047ThNLAqqAsHHWemfRnmgoF3xmzTRU5T6C7D
OS7aN7Woo6YEqgfaqawT4am8ewCrPuz30yj6yxvxX4SJPVvWIN1UPMp0bVGtk+OH
Az5IrWELuYqHb+apbGz5K7+wfp8AgbZcVjhhABEBAAG0QGpvYnMgYXQgaG82MDAg
KGpvYnMgYXQgaG82MDApIDxqb2JzLmF0LmhvNjAwQGV4YW0ueXVlaC1jYWtlLmNv
bT6JAT4EEwECACgFAlheeSkCGwMFCQeEzgAGCwkIBwMCBhUIAgkKCwQWAgMBAh4B
AheAAAoJEEt4GDVxQkv5vAsH/18J7BFE7GhRalOD+dkgRsHG1h653Ve3T0HJIebC
6xaHN80A+0TNdZVPlcyphBOskjkCHT85fH5wEASGwXe/4nbUcwncX4sNSj2D2BXn
546bWRxAqGrBF+2krofuO9C/Ojt6BuyKZtQux3NkcpMLEHza55ip5DxxP/e54F/E
XUOI0GnYgHyayGihVXJWahYVFebm4wgJ5iK4Wn9SP67GU5H57+9Ko2FJBaT0yNkb
SSxOIZKx8ZxCtgxCIEEOLG4wX4MkmsFz5xwfQmI47bniyZH1Qemo6JOg5df31B25
Hzp5Gb4vpmFA6vQPPf5fFmud0oIjp9Tn5ayt+C3gSAZYWX65AQ0EWF55KQEIAPje
AbEzlXxBn2/p3y/bmOLUnL9K8rjAi0DkZs+ech3BNNIHaqZoJG/YfztYVM1dKhoM
tCiivT1M4KIGHCG3mQd4MsCGIBnEAEj4hJWqUR9DKLEgaCJzXpBwzencBlMqa6tq
BPuXK2efo1hQZIlHj3tXaug+DfSp72FIHyfd99ZWSuIr8BUKt5Q5Mi9ZijYBqSmB
uoEbT+S38Wt2yM9uhsXkpkp7RzSIXFl3wHcwtodJX/lQUwNzccAM5WYr9P0r90+t
x2TwlUGsXlg3LWasfG8b7US0niIj5nYePQZbH578myqPFI9M/1NTVZu/HX/bX7oe
vgYKYqZ9d46AhXBeIW0AEQEAAYkBJQQYAQIADwUCWF55KQIbDAUJB4TOAAAKCRBL
eBg1cUJL+dV6B/9N7ED4z80avr+7U19WKGacZWG0cRjxofto97C4OYISIF34WZ4+
HOv2Ga8YA0cmt2QARLyphfBGrsiLVrpxHv7YLNI214OoKXuZWlxbZMi9A6qFkWvA
7FM5vOSnKSgMdRGgIsJuSPtoMzj9DwlT+SdWi4GfhzHXTNVtG3V20yGg2kUrMYBx
T7geH/wL6hUemqbg64Faj8jwDeyECdB7ZOahQxmXC/AVM+heSTkG/kQlFYEfB2Ib
t1oxguaoSNa1lV4ju4M0QI6nI/NQe5g9tBs/1+dyJNMovjmOh9S6DwulO4qyqaTZ
L/1fMojRuozzHbiIjAF+3VzPrCrwIK82s9bV
=UVi+
-----END PGP PUBLIC KEY BLOCK-----'''

QUESTIONS = [
    u"""*** 第一階段請先回答 6 題，第二階段再回答 2 題 ***
""",
    u"""
Subject1.
    
請建立一個 hg 或 git 的儲存庫，庫內的檔案將包含你接下來要回答的 7 個題目，除 Subject1 外，其餘題目皆須對應 1 個檔案或是 1 個資料夾，其順序須照考題順序。

數學題為加分題，可不寫，但仍須對應 1 個檔案。

在作 commit 時，請填寫合宜的說明、使用應聘帳號作為 committer ，並選擇在適當的時機，表現你懂得使用 branch 及 merge 功能，最終在 default branch(hg) 或是 master branch(git) 顯示你的所有答案。此儲存庫在回傳給考試委員前，請注意要消除 remote(push) url 的蹤跡。
""",
    u"""
使用 Django 、 Bootstrap 及其他開放源始碼工具建構一個網站，該網站只有一個頁面，該頁面只有一個表單、一個列表，頁面功能有兩個： 可留言、留言後的內容列表顯示在該頁面。建構此網站時，需使用 virtualenv ，並用 pip freeze > requirements.txt 紀錄所用的開放源始碼函式庫，而其他的 js/css 函式庫請直接加進儲存庫。
""",
    u"""
In this recruitment web site: We ask you to send the 14-digits md5 code. Please describe the reason about the 14-digits, why not choose 13-digits or 15-digits or anything else?
""",

    u"""
用 Python 撰寫一個遞迴函式。
""",

    u"""
600 是某數學問題的答案，請你推敲、說明「某數學問題」為何? 並以「敝司創辦人智力」為基準，為他列出求解過程。

「某數學問題」的難度愈高得分愈高，但若超過「敝司創辦人」智力所能理解的部份，那就會沒有分數。

給個提示，「敝司創辦人」不懂「Riemann integral」。
""",

    u"""
『議價』對敝下而言是件有點難的任務，所以我喜歡去 IKEA 而不愛去逛那種俗到脫褲的傢俱賣場，害怕買完後，是我被脫褲了。

人生中總會碰到『面議』這件事，像是買房子。湊巧的是，我們想要買的房子，是親戚的。要談出一個價格對我就是難事了，沒談成反正陌生的彼此也不再見面，還無所謂。

但現在得跟親戚談，想當然耳，他想出價高，而我想出價低，光是出價就可能影響感情，我出得太低，會不會讓他覺得我想佔他便宜，他出太高了，或許也怕像是要獅子大開口。大家都面臨到一個僵局： 誰要先走第一步?

於此，若是有一個公正第三人，站在我們中間，買賣雙方把價格告知第三人，如我的買價高於他的賣價，就直接公開雙方的買賣價，我們雙方再就買賣價範圍來『面議』，這樣傷感情的機率就大幅下降；

若是我的買價低於他的賣價，這樣「第三人」就直接銷毀字條，對我而言，只知道出得不夠高； 對他而言，也只知道出得不夠低，至於高低差多少， 1 塊錢還是 100 萬，都是有可能的。這感情要保全就不是難事。

然則此法取決於「第三人」有多公正。試想，在買價為 1700 萬，而賣價為 1500 萬時，若第三人有私心，宣佈此次報價未成交，事後再與賣家用 1550 萬購買，最後再用 1650 萬賣給買家，從中套利 100 萬，這兩邊不就成了冤大頭嗎?

這樣的難題，當然要上博碩網找答案囉~ 結果，我還真的找到解法，但受限於它的數學模型是給研究生看的，我要懂也得花大功夫，親戚要相信我拿這種數學不是要呼嚨他，這難度不亞於解決僵局，況且，懂了數學後，還得寫出程式才能完備整套模型。這其實是搞了別的問題來解決問題。

我只好眉頭一皺，緊接著一個念頭閃入，自此解決這個僵局。於是，這就成了各位的考題了。

請提出一套方法、流程或是模型，在不依賴公正第三人(或是單一裝置)的條件下，能判斷買賣雙方的價格是否成交，成交則公開買賣價，未成交則銷毀雙方價格數據，簡單講，在你的方法、流程或是模型中，不能有「一個人」或是「一項裝置」同時得知買價及賣價，但若是你的方法、流程或是模型真得只能依賴一位第三人(或是單一裝置)，那就請提出那人(或裝置)的「公正驗證方法」。而且限定所擬出的方法、流程、模型或是公正驗證方法，不得使用超過一般大學生能懂的數學，所用的數學愈簡單，分數愈高。
"""
]


def send_notice(email='', filename=''):
    ses = boto3.client('ses', region_name='us-west-2')
    body = '''<a href="mailto:%(email)s">%(email)s</a>''' % {'email': email}
    ses.send_email(Source='service@ho600.com',
                   Message={
                       'Subject': {
                           'Data': 'Applicants(%s) send %s' % (email, filename),
                           'Charset': 'utf-8'
                       },
                       'Body': {
                           'Text': { 'Data': body, 'Charset': 'utf-8' },
                           'Html': { 'Data': body, 'Charset': 'utf-8' }
                       }
                   },
                   Destination={ 'ToAddresses': ['hoamon@ho600.com'] })


def lambda_handler(event, context):
    """
    :param event:
    :param context:
    :return:

    INFO: pgpdump has problem on parse expiration_time.
    """
    public_key_content = event.get('public_key_content', '')
    filename = event['filename']
    if filename != '0A.asc' and filename[1] == 'A':
        encrypt_content = event['encrypt_content']
        encrypt_file_key_id_list = []
        for pkeskp in list(AsciiData(encrypt_content).packets()):
            encrypt_file_key_id = getattr(pkeskp, 'key_id', '')[-8:].upper()
            if encrypt_file_key_id: encrypt_file_key_id_list.append(encrypt_file_key_id)
        if len(encrypt_file_key_id_list) != 2:
            return {'status': 403, 'message': '403 Forbidden: PublicKeyCountError'}
        encrypt_file_key_id_list.remove(PUBLIC_KEY_ID)
        public_key_file_key_id = encrypt_file_key_id_list[0]
        dynamo = boto3.resource('dynamodb').Table(DYNAMODB_TABLE)
        response = dynamo.get_item(Key={'email': public_key_file_key_id,
                                        'type': 'reverse-apply-account-at-exam.yueh-cake.com'})
        item = response.get('Item', {})
        if not item:
            return {'status': 403, 'message': '403 Forbidden: PublicKeyID DoesNotExist'}
        email = item.get('public_key_id_email', '')
        if not email:
            return {'status': 403, 'message': '403 Forbidden: EmailDoesNotExist'}

        s3 = boto3.client('s3')
        _key = '%s/%s-%s/%s' % (S3_LOCATION, email, public_key_file_key_id, filename)
        try:
            s3.head_object(Bucket=S3_BUCKET, Key=_key)
        except:
            response = s3.put_object(
                ACL='public-read',
                Body=encrypt_content,
                Bucket=S3_BUCKET,
                ContentType='text/plain',
                Key=_key,
                StorageClass='STANDARD',
            )
            send_notice(email=email, filename=filename)
            return {'status': 200, 'message': filename}
        else:
            return {'status': 403, 'message': filename + ' was exist'}

    elif filename == '0A.asc':
        ad = AsciiData(public_key_content)
        adps = list(ad.packets())
        pub_algorithm_type = adps[0].pub_algorithm_type.lower()
        raw_pub_algorithm = adps[0].raw_pub_algorithm
        user_name = adps[1].user_name.lower()
        user_email = adps[1].user_email.lower()
        public_key_file_key_id = adps[3].key_id[-8:].upper()
        print("public_key_file_key_id: "+public_key_file_key_id)

        if pub_algorithm_type != 'rsa' or raw_pub_algorithm != 1:
            return {'status': 403, 'message': '403 Forbidden: PublicKey TypeError'}
        if re.sub('(applicants|[ \(\)])', '', user_name):
            return {'status': 403, 'message': '403 Forbidden: PublicKey UserNameError, It should be "applicants (applicants) <%s>"'%user_email}

        dynamo = boto3.resource('dynamodb').Table(DYNAMODB_TABLE)
        response = dynamo.get_item(Key={'email': user_email,
                                        'type': 'apply-account-at-exam.yueh-cake.com'})
        item = response.get('Item', {})
        if not item:
            return {'status': 403, 'message': '403 Forbidden: PublicKey EmailAddressDoesNotExist'}
        elif (int(item['timestamp']) + 86400) < int(time()):
            return {'status': 403, 'message': '403 Forbidden: EmailAddressExpiration'}
        elif item.get('public_key_id', ''):
            return {'status': 403, 'message': '403 Forbidden: PublicKeyAlreadyExist'}

        encrypt_content = event['encrypt_content']
        encrypt_file_key_id_list = []
        for pkeskp in list(AsciiData(encrypt_content).packets()):
            encrypt_file_key_id = getattr(pkeskp, 'key_id', '')[-8:].upper()
            if encrypt_file_key_id: encrypt_file_key_id_list.append(encrypt_file_key_id)
        if len(encrypt_file_key_id_list) != 2:
            return {'status': 403, 'message': '403 Forbidden: PublicKeyCountError'}
        elif PUBLIC_KEY_ID not in encrypt_file_key_id_list or public_key_file_key_id not in encrypt_file_key_id_list:
            return {'status': 403, 'message': '403 Forbidden: PublicKeyUsageError'}

        s3 = boto3.client('s3')

        response = s3.get_object( Bucket=S3_BUCKET, Key='%s/index.html' % S3_LOCATION)
        index_html = response['Body'].read()
        user_directory = '%s/%s-%s' % (S3_LOCATION, user_email, public_key_file_key_id)
        index_html = re.sub('<div id="build_version">.*</div>',
                            '<div id="create_time">Create Time at %s</div>'%datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S+UTC'), index_html)
        index_html = re.sub('(<textarea[^>]+name="public_key_content")></textarea>',
                            '\\1 readonly="readonly" style="background-color : #d1d1d1;">%s</textarea>'%public_key_content,
                            index_html)
        index_html = re.sub('<li[^>]+id="0A"[^>]+>', '<li id="0A">', index_html)

        response = s3.put_object(
            ACL='public-read',
            Body=index_html,
            Bucket=S3_BUCKET,
            ContentType='text/html',
            Key='%s/index.html' % user_directory,
            StorageClass='STANDARD',
        )
        response = s3.put_object(
            ACL='public-read',
            Body=public_key_content,
            Bucket=S3_BUCKET,
            ContentType='text/plain',
            Key='%s/public_key.asc' % user_directory,
            StorageClass='STANDARD',
        )
        response = s3.put_object(
            ACL='public-read',
            Body=encrypt_content,
            Bucket=S3_BUCKET,
            ContentType='text/plain',
            Key='%s/0A.asc' % user_directory,
            StorageClass='STANDARD',
        )

        dynamo.update_item(Key={'email': user_email,
                                       'type': 'apply-account-at-exam.yueh-cake.com'},
                                  UpdateExpression="set public_key_id = :public_key_id",
                                  ExpressionAttributeValues={":public_key_id":
                                                                 public_key_file_key_id},
                                  ReturnValues="UPDATED_NEW",
                                  )
        dynamo.put_item(Item={"timestamp": int(time()),
                              "email": public_key_file_key_id,
                              "public_key_id_email": user_email,
                              "type": 'reverse-apply-account-at-exam.yueh-cake.com'})
        if 0:
            Q1 = encrypt_text(random_q1(), public_keys=[PUBLIC_KEY_CONTENT, public_key_content])
            response = s3.put_object(
                ACL='public-read',
                Body=Q1,
                Bucket=S3_BUCKET,
                ContentType='text/plain',
                Key='%s/1Q.asc' % user_directory,
                StorageClass='STANDARD',
            )
            filename += " and 1Q.asc"
        send_notice(email=user_email, filename=filename)
        return {'status': 200, 'message': user_directory}
    else:
        return {'status': 403, 'message': 'FilenameError'}


def _clear_history():
    user_email = '54ca36c357a5c2aa175765f90fc51918@exam.yueh-cake.com'
    dynamo = boto3.resource('dynamodb').Table(DYNAMODB_TABLE)
    dynamo.delete_item(Key={"email": "3049DCE8",
                            "type": 'reverse-apply-account-at-exam.yueh-cake.com'})
    response = dynamo.update_item(
        Key={'email': user_email,
             'type': 'apply-account-at-exam.yueh-cake.com'},
        UpdateExpression='SET #timestamp = :timestamp, #public_key_id = :public_key_id',
        ExpressionAttributeNames={'#timestamp': 'timestamp', '#public_key_id': 'public_key_id'},
        ExpressionAttributeValues={
            ':timestamp': int(time()),
            ':public_key_id': None,
        },
        ReturnValues="UPDATED_NEW"
    )


def random_q1():
    Q1 = "\n".join(QUESTIONS[:2])
    BODY = QUESTIONS[2:]
    shuffle(BODY)
    for i, b in enumerate(BODY):
        Q1 += "\nSubject {}.\n".format((i+2))
        Q1 += b
    return Q1


def encrypt_text(text, public_keys=[PUBLIC_KEY_CONTENT]):
    return text


if __name__ == '__main__':
    _clear_history()
    d = {
        "public_key_content": open('3049DCE8.pkey.asc', 'r').read(),
        "filename": "0A.asc",
        "encrypt_content": open('id.txt.asc', 'r').read(),
         }
    print(json.dumps(d))
    print(lambda_handler(d, None))
