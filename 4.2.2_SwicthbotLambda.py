import json
import requests
import boto3

def lambda_handler(event, context):
    # パラメータストアから認証情報を取得
    ssm = boto3.client('ssm')
    token_param = ssm.get_parameter(Name='SWITCHBOT_TOKEN', WithDecryption=True)
    secret_param = ssm.get_parameter(Name='SWITCHBOT_SECURE', WithDecryption=True)

    token = token_param['Parameter']['Value']
    secret = secret_param['Parameter']['Value']

    # SwitchBot APIの設定
    url = "https://api.switch-bot.com/v1.0/devices"
    headers = {
        'Authorization': token,
        'client-secret': secret,
        'Content-Type': 'application/json'
    }

    # SwitchBot APIを呼び出し
    response = requests.get(url, headers=headers)

    print("Response from SwitchBot API:", response.json())

    return {
        'statusCode': 200,
        'body': json.dumps(response.json())
    }
