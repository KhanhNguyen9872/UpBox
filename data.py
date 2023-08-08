if __name__=='__main__':
    __import__('sys').exit()

class data:
    def __init__(self):
        self.token = ''
        self.username = ''
    def main_repo(self):
        return 'storage'
    def default_json(self, username, token):
        return \
        {
            'name_storage': 'upbox',
            'version': '1.0.0',
            'username': str(username),
            'token': str(token),
            'file' : {
                'upbox.txt': 'https://github.com/download/upbox.txt|sha'
            },
        }



        # Example file/folder
        # {
        #     'name_storage': 'upbox',
        #     'version': '1.0.0',
        #     'username': str(username),
        #     'token': str(token),
        #     'file' : {
        #         'file_name_1': json.dumps({
        #             'count': '2',
        #             'info': {
        #                 1: 'link|sha', 
        #                 2: 'link|sha',
        #             }
        #         }),
        #         'file_name_2': 'link|sha',
        #         'folder_1': {
        #             'file_name_1': 'link|sha',
        #             'file_name_2': 'link|sha',
        #         },
        #     },
        # }