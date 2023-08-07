import sys
if __name__=='__main__':
    sys.exit()

import requests, json, base64

# Disable Warning HTTPS Secure
__import__('urllib3').disable_warnings(__import__('urllib3').exceptions.InsecureRequestWarning)

head_json_origin = {'name_storage': 'upbox'}
main_repo = 'storage'
token = ''
username = ''

class Color:
    def white():return 'white'
    def black():return 'black'
    def blue():return 'blue'
    
def header_auth(t=""):
    if not t:
        t=token
    return {
        'user-agent' : 'curl/9.9.99',
        'Accept': 'application/vnd.github+json',
        'Authorization': 'token ' + t,
        'X-GitHub-Api-Version': '2022-11-28',
    }

def create_repo_github():
    payload = {
        'name': main_repo,
        'description': 'Storage by UpBox',
        'auto_init': 'true', 
        'private': 'true'
    }

    login = requests.post(
        'https://api.github.com/' + 'user/repos',
        auth=(username, token), 
        data=json.dumps(payload),
        verify=False,
    ).json()
    
    if login['full_name'] == "{}/{}".format(username, main_repo):
        return True
    return False
    
def check_token_github(token):
    if not token:
        return False
    if "#" in token:
        return False
    
    print("Token: {}".format(token))
    login = requests.get(
        'https://api.github.com/user', 
        headers=header_auth(token),
        verify=False,
    ).json()
    try:
        globals()["username"] = login['login']
        globals()["token"] = token
    except KeyError:
        print("Token Error!")
        return False
    
    if check_repo_exist():
        print("Repo exist!")
    else:
        print("Cannot create repo!")
    return True

def check_repo_exist():
    is_exist = False
    try:
        list_repo=requests.get(
            'https://api.github.com/search/repositories?q=user:{}'.format(username), 
            headers=header_auth(),
            verify=False,
        ).json()["items"]
    except KeyError:
        return create_repo_github()
    for repo in list_repo:
        if repo['name'] == main_repo:
            is_exist = True
            break
    if not is_exist:
        return create_repo_github()
    return is_exist

def get_username():
    return username

def get_file(file):
    return requests.get(
        'https://raw.githubusercontent.com/{}/storage/main/{}'.format(username, file),
        headers=header_auth(),
        verify=False,
    ).text
    
def delete_file(file, sha, message=""):
    if not message:
        message = "del - {}".format(file)

    query = requests.delete(
        'https://api.github.com/repos/{}/{}/contents/{}'.format(username, main_repo, file), 
        headers = header_auth(), 
        data = json.dumps({
            "message": str(message),
            "committer": {
                "name": username,
                "email": "{}@github.com".format(username)
            },
            "sha": str(sha)
        }),
    ).json()
    try:
        if not query['content'] == None:
            {}['upbox']
        query['commit']['sha']
        return True
    except KeyError:
        return False
def create_file(file, content="", message=""):
    if not message:
        message = "add - {}".format(file)
    query = requests.put(
        'https://api.github.com/repos/{}/{}/contents/{}'.format(username, main_repo, file), 
        auth = (username, token),
        headers = header_auth(), 
        data = json.dumps({
            "path": str(file),
            "message": str(message),
            "committer": {
                "name": username,
                "email": "{}@github.com".format(username)
            }, 
            "content": base64.b64encode(content.encode('utf8')).decode('utf8'), 
            "branch": "main"
        }),
    ).json()
    try:
        return [True, query['name'], query['sha'], query['size']]
    except KeyError:
        return [False]

def load_data():
    data = requests.get(
        'https://raw.githubusercontent.com/{}/storage/main/upbox.json'.format(username),
        headers = header_auth(),
        verify = False,
    ).text
    if data[:3] == "404":
        query = create_file('upbox.json', json.dumps(head_json_origin))
        if query[0]:
            data = head_json_origin
        else:
            print("Cannot create data!")
            return False
    print("data: {}".format(data))
    return data