import connection
import pickle

def encode(obj):
    wrapper = pickle.dumps(obj)
    wrapper_len = str(len(wrapper)).encode().rjust(4, b'0')
    return wrapper + wrapper_len