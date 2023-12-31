import json
import boto3
import requests

def lambda_handler(event, context):
    # SSMからWebhook URLを取得
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name='JIRA_WEBHOOK_URL', WithDecryption=True)
    webhook_url = parameter['Parameter']['Value']

    # イベントデータをJSON形式に変換
    event_data = json.dumps(event)

    # ヘッダーに'Content-Type': 'application/json'を設定
    headers = {'Content-Type': 'application/json'}

    # WebhookにデータをPOST（ヘッダーを含む）
    response = requests.post(webhook_url, data=event_data, headers=headers)

    # レスポンスをログに出力
    print("Response from webhook: ", response.text)

    return {
        'statusCode': 200,
        'body': json.dumps('Webhook sent successfully')
    }
