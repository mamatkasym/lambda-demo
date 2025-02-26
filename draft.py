import json, decimal

def decode_auth_token(auth_token: str):
    """Decodes the auth token"""
    try:
        # remove "Bearer " from the token string.
        auth_token = auth_token.replace("Bearer ", "")
        # decode using secret key, will crash if not set.
        print(auth_token)
        return jwt.decode(jwt=auth_token, key=SECRET, algorithms=["HS256"])

    except Exception:
        _LOG.info("Invalid token. Please log in again.")
        return

d = {
    "accessToken": "eyJraWQiOiJmbUoxdGdoZDczOFJ6VXZYeVRxMmRaWnNlV1RaT1p6UW9wVnNWYkFYZDVzPSIsImFsZyI6IlJTMjU2In0.eyJvcmlnaW5fanRpIjoiMDAyNWVkYmQtYzRiZi00ZTBiLTk4M2MtNDc0MjY2M2NiMTU5Iiwic3ViIjoiNzNlNGU4YTItODBmMS03MGEwLWEzZDAtYzY4Y2FhNGM2ZjFjIiwiYXVkIjoibm1zYnFoc2tiMG84bTkwN3QxanFzMjNmYyIsImV2ZW50X2lkIjoiMzc0MDA3MzMtYzFlMi00ZDVjLWFjN2EtYzNhZjBiMjhkZmFjIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NDA1NzI4OTgsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS1jZW50cmFsLTEuYW1hem9uYXdzLmNvbVwvZXUtY2VudHJhbC0xXzZ3ZnFScmFiNiIsImNvZ25pdG86dXNlcm5hbWUiOiJlbWFpbEBnbWFpbC5jb20iLCJleHAiOjE3NDA1NzY0OTcsImlhdCI6MTc0MDU3Mjg5OCwianRpIjoiODA4OGYzMTQtOGNjZC00YjQxLTk4NTQtNjFjZGI1Y2Y1YTZkIn0.waFH-JmSNVmO2zVNdBsYmEYwaF9HKPkhw6-n4VGUoXEc0_yZxFrDgFIdThielgP0tnvxQormsDg12UNEXEM3VQK67VWRD5cCnZKgf3zwpxkteh9qDUxhklKU3C-VpYRATucmYZUdXAvgExu4k7CLVgQou5vhhWa5AwfOai2EY8Xkqm6ME4wBn6XPsJc5AwsfK4YjHfWSfrr1hJ1WbftXS4wLN5exWRiDbMz_o9xCMg6FFPJfZ0tGKhWSNocBryR9H239sOHKIe8hpDoxfZOHDV2WAFsBMrXy9Wcl6XnBh-0lA-jwc-y-0xvvQmxqvJhBYIkPMWvEXDJheeLeTM4qJQ"
}

print(d["accessToken"])