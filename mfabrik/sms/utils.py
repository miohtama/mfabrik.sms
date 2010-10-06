from StringIO import StringIO
import random

try:
    # Python >= 2.5
    from hashlib import md5
except ImportError:
    # Python < 2.5
    from md5 import md5
    
    
def calculate_call_signature(params):
    """ Secure calls to mFabrik SMS server by hash signing params with API key.
    
    (id+from+to+to_alias+time+content+notify+response+response_time+multiple_responses+SSK)
    """    
    
    param_keys = "id+from+to+to_alias+time+content+notify+response+response_time+multiple_responses+SSK".split("+")
    
    concat = StringIO() 
    for key in param_keys:
        value = params.get(key, None)
        if value:
            concat.write(value)
            
    concat = concat.getvalue()
    
    hash = md5(concat).hexdigest()
    
    return hash

def get_random_id():
    """
    Generate unique id across space and time.
    """
    return random.randint(0, 2**31)

def stringify(dict):
    """ Force all dict values to ASCII strings.
    """
    
    for key, value in dict.items():
        dict[key] = str(value)
                