import requests
from getlinkedinauth import auth, headers

credentials = 'blog/somescripts/credentials.json'
access_token = auth(credentials) # Authenticate the API
headers = headers(access_token) # Make the headers to attach to the API call.

def user_info(headers):
    '''
    Get user information from Linkedin
    '''
    response = requests.get('https://api.linkedin.com/v2/me', headers = headers)
    user_info = response.json()
    return user_info
 
# Get user id to make a UGC post
user_info = user_info(headers)
urn = user_info['id']

author = f'urn:li:person:{urn}'

api_url = 'https://api.linkedin.com/v2/ugcPosts' # Modify depending what post you want to make

message = 'Preparing a LinkedIn Bot'

post_data = {
    "author": author,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": message
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

if __name__ == '__main__':
    r = requests.post(api_url, headers=headers, json=post_data)
    r.json()