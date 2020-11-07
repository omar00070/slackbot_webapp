import requests
import json

#BearerAuth class
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = f'Bearer {self.token}'
        return r


#main slack class
class Slack:

    def __init__(self, token, auth):
        self._token = token
        self.auth = auth
        self.urls = {
        'sendMessage':'https://slack.com/api/chat.postMessage',
        'getConversations': 'https://slack.com/api/conversations.list',
        'uploadFile': 'https://slack.com/api/files.upload'
         }

    def get_conversations(self):
        '''
            method to get a list of the public conversations in the slack chat
            parameters: self
            returns: a python dict object in the format {'conversation_name': 'conversation_id'}
        '''
        res = requests.get(
            self.urls['getConversations'], 
            auth=self.auth)
        res_json = res.json()
        channels = {channel['name']: channel['id'] for channel in res_json['channels']}
        
        if not res_json['ok']:
            print(res_json['error'])
        
        return channels, res
    
    def send_message(self, content, channel_id):
        '''
            method to send messages to a slack channel
            parameters: slef, content: str of the message, channel_id: str of the channel ID
            returns: response object
        '''
        headers = {"Content-type": "application/json"}
        payload = {
            "channel": channel_id,
            "text": content,
        }
        data = json.dumps(payload)
        res = requests.post(
            self.urls['sendMessage'],
            auth=self.auth, 
            headers=headers, data=data
            )
        
        res_json = res.json()
        if not res_json['ok']:
            print(res_json['error'])
        
        return res

    def send_file(self, channels, file, text=None):
        '''
        TODO: send files using a more customisable method to add more than just one
        string

            method to send files to slack channels
            parameters: 
                channels: str of comma separated values for channel ids
                file_path: str of the path to the file
                text: str of the message that is going to be shown above the file,
                this method is limited to one string
            returns: response object
        '''
        
        files = {'file': file}
        data = {
            'channels': channels,
            'initial_comment': text
        }
        res = requests.post(
            self.urls['uploadFile'], 
            auth=self.auth,
            data=data, 
            files=files
            )

        res_json = res.json()

        if not res_json['ok']:
            print(res_json['error'])

        return res