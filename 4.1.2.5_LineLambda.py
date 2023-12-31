import json
import os
import requests
import boto3

def get_ssm_parameter(name):
    # SSMクライアントの作成
    ssm = boto3.client('ssm')
    # パラメータの取得
    parameter = ssm.get_parameter(Name=name, WithDecryption=True)
    return parameter['Parameter']['Value']

def lambda_handler(event, context):
    # SSMパラメータストアからLINEのアクセストークンとユーザーIDを取得
    line_token = get_ssm_parameter('LINE_ACCESS_TOKEN')
    line_user_id = get_ssm_parameter('LINE_USER_ID')

    # LINE APIのエンドポイント
    line_api_url = 'https://api.line.me/v2/bot/message/push'

    # LINEに送信するメッセージを作成
    message = {
        'to': line_user_id,
        'messages': [
            {
                'type': 'text',
                'text': json.dumps(event)  # AWSイベントを文字列に変換
            }
        ]
    }

    # LINE APIへのリクエストヘッダー
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {line_token}' 
    }

    # LINE APIにリクエストを送信
    try:
        response = requests.post(line_api_url, headers=headers, data=json.dumps(message), timeout=10)  # 10秒のタイムアウト
        response.raise_for_status()  # ステータスコードが200以外の場合に例外を発生させる
    except requests.exceptions.Timeout:
        print("Request timed out")
        return {
            'statusCode': 408,
            'body': json.dumps('Request timed out')
        }
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Request failed')
        }
