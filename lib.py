import sys
if __name__=='__main__':
    sys.exit()

stdout_sys = sys.stdout
import requests, json, base64, random, datetime, pathlib, os, shutil, time, subprocess, threading
import data as data_default
data = data_default.data()

debug_mode = True
tmp_path = "tmp"
working_dir = os.getcwd()

# Disable Warning HTTPS Secure
__import__('urllib3').disable_warnings(__import__('urllib3').exceptions.InsecureRequestWarning)

# Create tmp folder
try:
    shutil.rmtree(tmp_path)
except:
    pass
try:
    os.mkdir(tmp_path)
except:
    pass

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

def getTimeNow():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
          
def addLog(message = ""):
    try:
        message = message.encode('utf8')
    except UnicodeEncodeError:
        message = message.encode('utf8')
    open("log.txt", "ab").write(message)
      
def debug(message = "", content = ""):
    if debug_mode:
        print("DEBUG: {}".format(message))
    addLog("\n[{time}] {a} {b}".format(time = getTimeNow(), a = message, b = str(content)))

def random_str(length = 8):
    return "".join([random.choice("qwertyuiopasdfghjklzxcvbnm0987654321._-") for x in range(length)])

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
            'description': 'Storage by {}'.format(data.program_name()),
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

def rename_filename(file_name):
    new_name = ""
    tmp_lst = [str(char) for char in 'qwertyuiopasdfghjklzxcvbnm0987654321QWERTYUIOPASDFGHJKLZXCVBNM-_.+']
    for char in str(file_name):
        if char == ' ':
            char = '.'
        elif char in ['(', ')', '|', '\\', '/', '"', '[', ']', '{', '}', ',', '\'', ';', '`', '~']:
            continue
        elif char not in tmp_lst:
            char = '.'
        new_name = new_name + char

    return new_name
    
def update_data(type_, file_name, tag_name = None):
    # type: add, del, edit #
    if tag_name == None:
        tag_name = "hostfile"
    tmp_json = get_data()
    file_name = rename_filename(file_name)
    debug("update data ({type_} {file})".format(type_ = type_, file = file_name))
    if str(type_) == 'add':
        tmp_js_file = {}
        release_id = check_release_exist(tag_name)
        if (release_id == False):
            debug("Cannot get release id from [{tag}]".format(tag = tag_name))
            return False
        info = get_info_file_release(file_name, release_id)
        if info == False:
            debug("Network Error [{file}]".format(file = file_name))
            return False
        elif info == -1:
            debug("File not found [{file}]".format(file = file_name))
            update_data('del', file_name)
            return False

        tmp_js_file['count'] = 1
        tmp_js_file_info = {}
        for index in range(tmp_js_file['count']):
            tmp_js_file_info[index] = "{id}|{node_id}|{size}|{created_at}|{updated_at}|{download_count}".format(
                id = str(info['id']),
                node_id = info['node_id'],
                size = info['size'],
                created_at = info['created_at'],
                updated_at = info['updated_at'],
                download_count = info['download_count']
            )
        tmp_js_file['info'] = tmp_js_file_info
        
        tmp_json['file'][str(file_name)] = json.dumps(tmp_js_file)
        set_data(tmp_json)

        # for i in range(0, len(path), 1):
        #     if not str(path[i]):
        #         break
        #     tmp_str = tmp_str + "['" + str(path[i]) + "']"
        #     txt = tmp_str + " = {{'{0}': ''}}".format(path[i])
        #     print(txt)
        #     exec(txt)
        # txt = tmp_str + "['{}'] = {}".format(query[0], str(json.dumps({
        #          'count': '1',
        #          'info': {
        #             '1': 'https://raw.githubusercontent.com/{{}}/{{}}/main/|{}|{}'.format(query[1], query[2]),
        #          }
        # }).encode('utf8'))[1:])
        # print(txt)
        # exec(txt)
        
    elif str(type_) == 'del':
        try:
            del tmp_json['file'][file_name]
        except KeyError:
            debug("Cannot delete data [{file}] because not found!".format(file = file_name))
            return False
    elif str(type_) == 'modify':
        pass
    set_data(tmp_json)
    remove_file_release(
        '{}.json'.format(program_name().lower()),
        "config"
    )
    create_file_release(
        '{}.json'.format(program_name().lower()),
        json.dumps(get_data()),
        "config"
    )
    return True
    
def get_data():
    return data.storage_data

def set_data(data_):
    data.storage_data = data_

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
    
def get_info_file_release(file_name, release_id) -> int:
    query = requests.get(
        "https://api.github.com/repos/{user}/{repo}/releases/{tag}/assets?name={file_name}".format(user = data.username, repo = data.main_repo(), tag = release_id, file_name = file_name),
        headers = header_auth(),
        verify = False,
    )
    if (query.status_code == 200):
        query = query.json()
        for obj in query:
            if (obj['name'] == file_name):
                query = obj
                break
        print(query)
        try:
            int(query['id'])
            return query
        except (ValueError, TypeError):
            return -1
    else:
        return False
    
def get_data_from_release(file_name, tag_name = None) -> list:
    if tag_name == None:
        tag_name = "hostfile"
    release_id = check_release_exist(tag_name)
    if release_id == False:
        release_id = create_release(tag_name)
    
    id_file = get_info_file_release(file_name, release_id)
    
    if id_file == -1:
        debug("File not found [{file}]".format(file = file_name))
        update_data('del', file_name)
        return [404, b'']
    elif (id_file != False):
        id_file = id_file['id']
        headers = header_auth()
        headers["Accept"] = "application/octet-stream"
        query = requests.get(
            "https://api.github.com/repos/{user}/{repo}/releases/assets/{id}".format(user = data.username, repo = data.main_repo(), id = id_file),
            headers = headers,
            verify = False,
        )
    else:
        return [404, b'']
    return [query.status_code, query.content]
    
def load_data():
    debug("load data....")
    query = get_data_from_release(program_name().lower() + ".json", "config")
    debug(query[1].decode('utf8'))
    if query[0] == 404:
        query = create_file_release(
            '{}.json'.format(program_name().lower()), 
            json.dumps(data.default_json()),
            "config"
        )
        if query:
            query = json.dumps(data.default_json())
            set_data(json.loads(query))
            create_file_release('readme.txt', 'Thanks for using UpBox!')
            update_data('add', 'readme.txt')
            return json.loads(query)
        else:
            debug("Cannot create data!")
            return False
    else:
        try:
            query[1] = query[1].decode('utf8')
        except UnicodeDecodeError:
            query[1] = query[1].decode('latin-1')
            
        set_data(json.loads(query[1]))
    return json.loads(query[1])

def upload_file_release(path_file, id = None):
    if (id == None):
        id = check_release_exist("hostfile")
        if (id == False):
            id = create_release()
    # if (id == None):
    #     id = check_release_exist("config")
    if (int(id) < 1):
        debug("cannot upload file, release id below 1 [{id}]".format(id = id))
        return False
    debug("upload [{file}] to release [{tag}]".format(file = path_file, tag = id))
    headers = header_auth()
    headers['Content-Type'] = "application/octet-stream"
    __file__ = open(path_file, 'rb')
    file_name = "/".join(path_file.split("\\")).split("/")[-1]
    query = requests.post(
        'https://uploads.github.com/repos/{user}/{repo}/releases/{release_id}/assets?name={file_name}'.format(user = data.username, repo = data.main_repo(), release_id = id, file_name = file_name), 
        headers = headers,
        data = __file__,
        verify = False,
    )

    __file__.close()
    if (query.status_code == 201):
        debug("Upload release completed!")
        return True
    try:
        if query.json()['code'] == "already_exists":
            debug("Cannot upload! file exists [{file}] from release [{tag}]".format(file = file_name, tag = id))
            return False
    except:
        pass
    debug("Upload release error!", str(query.text))
    return False

def check_release_exist(tag_name) -> int:
    # check release exist
    query = requests.get(
        'https://api.github.com/repos/{user}/{repo}/releases/tags/{tag}'.format(user = data.username, repo = data.main_repo(), tag = tag_name), 
        headers=header_auth(),
        verify=False,
    )
    if (query.status_code == 200):
        debug("Release [{tag}] exist!".format(tag = tag_name))
        return query.json()["id"]
    elif (query.status_code == 404):
        debug("Release [{tag}] not exist!".format(tag = tag_name))
        return False
    else:
        debug("Check release exists error!", str(query.text))
        return False
    
def delete_tag(tag_name = None) -> bool:
    query = requests.delete(
        'https://api.github.com/repos/{user}/{repo}/git/refs/tags/{tag}'.format(user = data.username, repo = data.main_repo(), tag = tag_name), 
        headers = header_auth(),
        verify=False,
    )
    if (query.status_code != 204):
        debug("cannot delete tag [{tag}]".format(tag = tag_name), query.status_code)
        return False
    
    debug("deleted tag [{tag}]".format(tag = tag_name))
    return True

def delete_release(tag_name = None) -> bool:
    release_id = check_release_exist(tag_name)
    if (release_id != False):
        query = requests.delete(
            'https://api.github.com/repos/{user}/{repo}/releases/{release_id}'.format(user = data.username, repo = data.main_repo(), release_id = release_id), 
            headers = header_auth(),
            verify=False,
        )
        if (query.status_code != 204):
            debug("cannot delete release [{tag}] with ID [{id}]".format(tag = tag_name, id = release_id), query.status_code)
            return False
    
    debug("deleted release [{tag}] with ID [{id}]".format(tag = tag_name, id = release_id))
    return True

def create_release(tag_name = None, name = "main", description = "None") -> int:
    if (tag_name == None):
        tag_name = "hostfile"
        name = "Host File"
    debug("create a release [{tag}]".format(tag = tag_name))
    release_id = check_release_exist(tag_name)
    if (release_id == False):
        # create release
        query = requests.post(
            'https://api.github.com/repos/{user}/{repo}/releases'.format(user = data.username, repo = data.main_repo()), 
            headers = header_auth(),
            json={
                "tag_name": str(tag_name),
                "target_commitish": "main",
                "name": str(name),
                "body": str(description),
                "draft": False,
                "prerelease": False,
                "generate_release_notes": False,
                "make_latest": "False"
            },
            verify=False,
        ).json()
        try:
            debug("Create release [{tag}] completed with ID [{id}]".format(tag = tag_name, id = query["id"]))
            return query["id"]
        except KeyError:
            debug("Cannot create release [{tag}]".format(tag = tag_name))
            return False
    return release_id

def create_file_release(file_name : str, data : bytes, tag_name = None) -> bool:
    rand_folder = random_str(48)
    file_path = "{path}/{folder}/{file}".format(path = tmp_path, folder = rand_folder, file = file_name)
    if (type(data) == type("")):
        data = data.encode('utf8')
    elif (type(data) == type(0)):
        data = str(data).encode('utf8')
    elif (type(data) == type(False)):
        data = str(data).encode('utf8')
    
    try:
        os.mkdir("{path}/{folder}".format(path = tmp_path, folder = rand_folder))
    except:
        pass
    open(file_path, 'wb').write(data)
    if tag_name == None:
        tag_name = "hostfile"
    release_id = create_release(tag_name)
    if (release_id == False):
        release_id = check_release_exist(tag_name)
    debug("create file release [{file}] to [{id}]".format(file = file_name, id = release_id))
    if (upload_file_release(file_path, release_id)):
        debug("completed create [{file}] to [{id}]".format(file = file_name, id = release_id))
        shutil.rmtree("{path}/{folder}".format(path = tmp_path, folder = rand_folder))
        return True
    debug("failed create [{file}] to [{id}]".format(file = file_name, id = release_id))
    shutil.rmtree("{path}/{folder}".format(path = tmp_path, folder = rand_folder))
    return False

def remove_file_release(file_name : str, tag_name = None) -> bool:
    if (tag_name == None):
        tag_name = "hostfile"
    release_id = check_release_exist(tag_name)
    if (release_id == False):
        debug("Release [{tag}] not found!".format(tag = tag_name))
        return False
    
    id_file = get_info_file_release(file_name, release_id)
    if (id_file == False):
        debug("Cannot get release info file [{file}]".format(file = file_name))
        return False
    
    id_file = id_file['id']
    query = requests.delete(
        'https://api.github.com/repos/{user}/{repo}/releases/assets/{id}'.format(user = data.username, repo = data.main_repo(), release_id = release_id, id = id_file), 
        headers = header_auth(),
        verify=False,
    )

    if (query.status_code != 204):
        debug("cannot delete file [{file}] from [{tag}] with ID [{id}]".format(file = file_name, tag = tag_name, id = release_id), query.text)
        return False
    
    debug("deleted file [{file}] from [{tag}] with ID [{id}]".format(file = file_name, tag = tag_name, id = release_id), query.status_code)
    return True

def get_list_file():
    tmp_dict = {}
    file = get_data()['file']
    for f in file:
        data = json.loads(file[f])
        try:
            data['count']
            tmp_dict[f] = "file"
        except KeyError:
            tmp_dict[f] = "folder"
    return tmp_dict