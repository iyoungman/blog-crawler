import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta

SENDER_EMAIL = "imiyoungman@daum.net"  # 발신자 이메일
RECIPIENTS_EMAIL_LIST = []
MAIL_TITLE = datetime.today().strftime('%Y-%m-%d') + " BLOG UPDATE"  # 메일 제목
MAIL_BODY = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d') + " 의 업데이트된 글 목록입니다."  # 메일 본문
ATTACHMENTS = {}
AWS_ACCESS_KEY = "AKIAJUIIKKBG5ZA2ILZA"  # AWS 키
AWS_SECRET_ACCESS_KEY = "X4hiWy3s/nzLPPlzeHom5OZ5DY64rZnSe8ZjId5W"  # AWS 키
AWS_REGION = "ap-southeast-2"  # AWS 리젼
SES_CLIENT = boto3.client('ses',
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION)


def send_email(recipients: list, attachments: dict):
    msg = MIMEMultipart()
    msg['Subject'] = MAIL_TITLE
    msg['From'] = SENDER_EMAIL

    part = MIMEText(MAIL_BODY)
    msg.attach(part)

    for attachment in attachments:
        part = MIMEApplication(open(attachments[attachment], 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=attachment)
        msg.attach(part)

    responses = []
    for recipient in recipients:  # 사용자에게 이메일 전송
        msg['To'] = recipient
        response = SES_CLIENT.send_raw_email(
            Source=SENDER_EMAIL,
            Destinations=[recipient],
            RawMessage={
                'Data': msg.as_string()
            })
        responses.append(response)
    return responses
