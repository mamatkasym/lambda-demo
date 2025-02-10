import boto3
temp_aws_access_key_id = "ASIA5FTZDTP2NW3HFO6Q"
temp_aws_secret_access_key = "5FgRKX501JGiEG9J2C34f5wnn1Kttl3UusiRwaLX"
temp_aws_session_token = "IQoJb3JpZ2luX2VjEJ7//////////wEaCXVzLWVhc3QtMSJHMEUCIHTTrb/SdJQZGJyP7huEheKvFfQDeVFCMqhbh9yKbTeWAiEA3FsstSlxCGzCGxdqz+I4b20WYsJa1N0b+WTF87SIPGMq8wIItv//////////ARAAGgw5MDU0MTgzNDk1NTYiDLvEujbRc979N5dMtSrHAvxFvzRkaT2gvA6amcBGcu1g5RwWPCo7DyLaneOmMo9OWZ9SISVQ9YovGWcsqOIjaTQbCLa10Q3OzYbpa/a0Z8IeAkGUF1DCU44V/QyoZUcjX3fEFZb0FRbizZfVOb4hLgB/jyzQlLokGxNupUFB1aj9++5UejQaeFa39rFmGsOS45LDJ8jkZ3IqITaj9K/L8T4hdkzZCpr5dZuk8e51ow95y0MX36TRH34dsm+L6VYsN5Z5n1gduFfxAOUjPA2lPi3H2Nu8Q0PIXwUls8QV+UN+gWDfmrwzz6b5XrKruQKZnUGxzV1AczeHqmHqhKgZ3Vx+tdMme2Mx10ZspC5VLA5vQrxeYgr9C9kz5OUbZ0T9EYa3DfE+V7Z8ouLdHVlTqx0rOoIVQckTPx3lTpqjXe4lVmYNvNsqmPxxnMIVGgtQw7Li35xosTCjlaa9BjqdAfK49ueL6S6Bz9udTxbxcBuKRSu93N6o4mN6X2OoFbozxzvFY2GHSb6JgO/TktIS/uhTeL3MARQghg9PmZVhoFs+hV6a3PNOn3wFzbdCIG4mUsTYcn7s+n/S/b0JknCRkRDAU4fwHrt0CaPBCLKIISlhbbYxMyNGc/MFwF96j2TIjptKZErQrIW/ODqQ6rTREqtfTKVeHhCRqnFV0TM="


dynamodb = boto3.resource('dynamodb', region_name="eu-central-1", aws_access_key_id=temp_aws_access_key_id,
                          aws_secret_access_key=temp_aws_secret_access_key, aws_session_token=temp_aws_session_token)

table = dynamodb.Table('cmtr-f88924dc-Events')

response = table.put_item(
    Item={
        'pk': 'id#1',
        'sk': 'cart#123',
        'name': 'SomeName',
        'inventory': 500,
        # ... more attributes ...
    }
)
print(response)
