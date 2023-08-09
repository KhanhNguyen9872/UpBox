if __name__=='__main__':
    __import__('sys').exit()

class data:
    def __init__(self):
        self.token = ''
        self.username = ''
        self.storage_data = ''
    def main_repo(self):
        return 'storage'
    def program_name(self):
        return 'UpBox'
    def default_json(self):
        return \
        {
            'name_storage': self.program_name().lower(),
            'version': '1.0.0',
            'username': str(self.username),
            'repo': str(self.main_repo()),
            'file' : {},
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