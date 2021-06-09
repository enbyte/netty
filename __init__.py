import connection
import pickle

def encode(obj):
    o = pickle.dumps(obj)
    length = str(len(o)).encode().rjust(4, b'0')
    return length + o
