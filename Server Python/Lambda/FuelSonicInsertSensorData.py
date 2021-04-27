import boto3
import json


def lambda_handler(event, context):
    request_body = event
    client = boto3.resource('dynamodb')
    table = client.Table('FuelSonicMasterDataTable')

    input = {'transactionID': request_body['transactionID'], 'reportType': request_body['reportType'],
             'packetSize': request_body['packetSize'], 'height': request_body['height'],
             'temperature': request_body['temperature'], 'batteryVoltage': request_body['batteryVoltage'],
             'RSPR': request_body['RSPR'], 'FRAM': request_body['FRAM'], 'IMEI': request_body['IMEI']}
    print(request_body)
    # table.put_item(Item=input)

    body = {
        'text': 'Successfully submitted to Database'
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
