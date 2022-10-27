import jwt, json # $ pip3 install pyjwt

def decode(jwt_token: str):
    try:
        decoded = jwt.decode(jwt_token, options={'verify_signature': False} , algorithms=["HS256"])
        #parse
        user = json.loads(decoded["user"])
        for k, v in user.items():
            print(k, ':', v)
        #next page
        input(">>> ")
        return user["displayName"], decoded["exp"]
    except jwt.exceptions.DecodeError:
        print("invalid jwt token")
        exit()
