import os, requests

def token(request):
    if not "Authorization" in request.headers:
        return None, ("No credentials provided", 401)
    
    token = request.headers["Authorization"] # Get the JWT token from the request headers

    print("token = ", token)

    if not token:
        return None, ("No credentials provided", 401)
    
    response = requests.post(f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate", headers={"Authorization": token}) # Send a POST request to the auth service to validate the token

    if response.status_code == 200:
        return response.text, None # response.text contains the json object of the payload of the JWT token
    else:
        return None, (response.text, response.status_code)