
d = {'eventID': 'a6413096a1f5e6a352ff4d0a8c4a757b', 'eventName': 'INSERT', 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'eu-central-1', 'dynamodb': {'ApproximateCreationDateTime': 1739173754.0, 'Keys': {'id': {'S': '1'}}, 'NewImage': {'id': {'S': '1'}, 'value': {'N': '142398'}, 'key': {'S': 'TR_DANA'}}, 'SequenceNumber': '2100000000059121242208', 'SizeBytes': 25, 'StreamViewType': 'NEW_AND_OLD_IMAGES'}, 'eventSourceARN': 'arn:aws:dynamodb:eu-central-1:905418349556:table/cmtr-f88924dc-Configuration/stream/2025-02-10T07:47:33.810'}

print(d["dynamodb"]["NewImage"])