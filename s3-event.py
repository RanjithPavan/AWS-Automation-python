# coding: utf-8
event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2020-07-14T17:14:45.526Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDA4PSXFYWBYJQ7XLE3N'}, 'requestParameters': {'sourceIPAddress': '97.117.154.249'}, 'responseElements': {'x-amz-request-id': '4DB763C8D8CFD89F', 'x-amz-id-2': 'yF4HAT462yIF9wdp/ORvAw7MO8x2JRsXhql7YerbZ1lpqqzRuc1ZNaAmHzhlDG7l1pRW75ffAyFmCOkcEnsQmCERwQn84zbA'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': '52dcf339-9141-41e9-b7ed-e6bc3708b016', 'bucket': {'name': 'ranjithvideoanalyzer1', 'ownerIdentity': {'principalId': 'AIVTNZWKZNCFC'}, 'arn': 'arn:aws:s3:::ranjithvideoanalyzer1'}, 'object': {'key': 'Blurry.mp4', 'size': 4145766, 'eTag': '2b967fdf9555a4f919236b478cf3aed4', 'sequencer': '005F0DE80085381F89'}}}]}
event
event['Records'][0]['s3']['bucket']['name']
event['Records'][0]['s3']['object']['key']
