import bcrypt

class Message:
    def __init__(self, data_dict):
        self.uid = data_dict['uid']
        self.data = data_dict['data']
        self.time = data_dict['time']
        self.message_type = data_dict['type']

    def __getitem__(self, index):
        if index == 'uid':
            return self.uid
        elif index == 'data':
            return self.data
        elif index == 'time':
            return self.time
        elif index == 'type':
            return self.message_type
        else:
            raise KeyError("Message indices must be 'uid', 'data', 'time', or 'type'! Unrecognized item %s" % index)
        
    
def cute_name(uid_str):
    return uid_str[:10]

def gen_hash_salt():
    return bcrypt.gensalt()

def generate_random_uid(string):
    return bcrypt.hashpw(string.encode(), gen_hash_salt()).decode('utf-8')