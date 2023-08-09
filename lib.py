import sys
if __name__=='__main__':
    sys.exit()

stdout_sys = sys.stdout
import requests, json, base64
import data as data_default
data = data_default.data()

debug_mode = True

# Disable Warning HTTPS Secure
__import__('urllib3').disable_warnings(__import__('urllib3').exceptions.InsecureRequestWarning)

class Color:
    def __init__(self, is_gui=True):
        self.is_gui = is_gui
        self.color = {
            # GUI : Terminal #
            'white': '\033[0m',
            'violet': '\033[95m',
            'black': '\033[30m',
            'blue': '\033[94m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'green': '\033[32m',
        }
        
    def getcolor(self, color):
        if self.is_gui:
            return list(self.color)[list(self.color).index(color)]
        else:
            return self.color[color]
            
def debug(message=""):
    if debug_mode:
        print("DEBUG: {}".format(message))

def header_auth(t=""):
    if not t:
        t = data.token
    return {
        'user-agent' : 'curl/9.9.99',
        'Accept': 'application/vnd.github+json',
        'Authorization': 'token ' + t,
        'X-GitHub-Api-Version': '2022-11-28',
    }

def create_repo_github():
    query = requests.post(
        'https://api.github.com/user/repos',
        auth=(data.username, data.token), 
        data=json.dumps({
            'name': data.main_repo(),
            'description': 'Storage by {}'.format(data.main_repo()),
            'auto_init': 'true', 
            'private': 'true'
        }),
        verify=False,
    ).json()
    
    if query['full_name'] == "{}/{}".format(data.username, data.main_repo()):
        return True
    return False
    
def check_token_github(token):
    if not token:
        return False
    if "#" in token:
        return False
    
    debug("Token: {}".format(token))
    query = requests.get(
        'https://api.github.com/user', 
        headers=header_auth(token),
        verify=False,
    ).json()
    try:
        data.username = query['login']
        data.token = token
    except KeyError:
        debug("Token Error!")
        return False
    
    if check_repo_exist():
        debug("Repo exist!")
    else:
        debug("Cannot create repo!")
    return True

def check_repo_exist():
    is_exist = False
    try:
        list_repo=requests.get(
            'https://api.github.com/search/repositories?q=user:{}'.format(data.username), 
            headers=header_auth(),
            verify=False,
        ).json()["items"]
    except KeyError:
        return create_repo_github()
    for repo in list_repo:
        if repo['name'] == data.main_repo():
            is_exist = True
            break
    if not is_exist:
        return create_repo_github()
    return is_exist

def get_username():
    return data.username

def program_name():
    return data.program_name()

def get_file(file):
    return requests.get(
        'https://raw.githubusercontent.com/{}/storage/main/{}'.format(data.username, file),
        headers=header_auth(),
        verify=False,
    ).text
    
def delete_file(file, sha, path="", message=""):
    if not message:
        message = "del - {}".format(file)
    if not path:
        path = str(file)
    else:
        path = path + "/" + str(file)
        
    print(sha)
        
    query = requests.delete(
        'https://api.github.com/repos/{}/{}/contents/{}'.format(data.username, data.main_repo(), path), 
        headers = header_auth(), 
        data = json.dumps({
            "message": str(message),
            "committer": {
                "name": data.username,
                "email": "{}@github.com".format(data.username)
            },
            "sha": str(sha)
        }),
    ).json()
    print(query)
    try:
        if not query['content'] == None:
            {}[program_name().lower()]
        query['commit']['sha']
        return True
    except KeyError:
        return False
    
def create_file(file, content="", path="", message=""):
    if not message:
        message = "add - {}".format(file)
    if not path:
        path = str(file)
    else:
        path = path + "/" + str(file)
    payload = {
        "message": str(message),
        "committer": {
            "name": data.username,
            "email": "{}@github.com".format(data.username)
        }, 
        "content": base64.b64encode(content.encode('utf8')).decode('utf8'), 
        "branch": "main"
    }
    query = requests.put(
        'https://api.github.com/repos/{}/{}/contents/{}'.format(data.username, data.main_repo(), path), 
        auth = (data.username, data.token),
        headers = header_auth(), 
        data = json.dumps(payload),
    ).json()
    print(query)
    try:
        return [True, query['content']['name'], query['content']['sha'], query['content']['size']]
    except KeyError:
        return [False]
    
def update_data(type, query, path=""):
    # type: add, del, edit #
    tmp_str = "tmp_json['file']"
    tmp_json = data.storage_data
    path = path.split("/")
    if str(type) == 'add':
        for i in range(0, len(path), 1):
            if not str(path[i]):
                break
            tmp_str = tmp_str + "['" + str(path[i]) + "']"
            txt = tmp_str + " = {{'{0}': ''}}".format(path[i])
            print(txt)
            exec(txt)
        txt = tmp_str + "['{}'] = {}".format(query[0], str(json.dumps({
                 'count': '1',
                 'info': {
                    '1': 'https://raw.githubusercontent.com/{{}}/{{}}/main/|{}|{}'.format(query[1], query[2]),
                 }
        }).encode('utf8'))[1:])
        print(txt)
        exec(txt)
        
    elif str(type) == 'del':
        pass
    elif str(type) == 'edit':
        pass
    data.storage_data = tmp_json
    create_file(
        '{}.json'.format(program_name().lower()),
        json.dumps(data.storage_data),
        '',
    )
    return True
    
def get_data():
    return data.storage_data

def set_data(data):
    data.storage_data = data
    
def add_data(file, data="", path=""):
    query = create_file(file, data, False, path)
    if query[0]:
        update_data('add', query[1:], path)
    else:
        debug("Cannot add data!")
        return False
    return True

def edit_data(file, sha, data="", path=""):
    if delete_file(file, sha, path):
        create_file(file, data, path)
    else:
        debug("Cannot modify file!")
    # query = create_file(file, data, True, path, sha, "edit - {}".format(file))
    # if query[0]:
    #     update_data('add', query[1:])
    # else:
    #     debug("Cannot edit data!")
    #     return False
    # return True
    
def load_data():
    query = requests.get(
        'https://raw.githubusercontent.com/{}/storage/main/{}.json'.format(data.username, program_name().lower()),
        headers = header_auth(),
        verify = False,
    ).text
    print(query)
    if query[:3] == "404":
        query = create_file(
            '{}.json'.format(program_name().lower()), 
            json.dumps(data.default_json()),
            '',
        )
        if query[0]:
            query = json.dumps(data.default_json())
            data.storage_data = json.loads(query)
            add_data('readme.txt', 'Thanks for using UpBox!')
        else:
            debug("Cannot create data!")
            return False
    else:
        data.storage_data = json.loads(query)
    #edit_data('readme.txt', json.loads(data.storage_data['file']['readme.txt'])['info']['1'].split("|")[1], "hehee", "")
    #add_data('test_pasath.txt','haaaa','folder')
    return json.loads(query)
