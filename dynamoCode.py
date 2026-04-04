import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('packers_pageviews')

def log_page_view(page_name, user_ip):
    table.put_item(
        Item={
            'page': page_name,
            'timestamp': datetime.utcnow().isoformat(),
            'user_ip': user_ip
        }
    )

def get_page_view_count(page_name):
    response = table.query(
        KeyConditionExpression=Key('page').eq(page_name)
    )
    return len(response['Items'])