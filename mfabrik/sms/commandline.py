"""

    Send SMS messages from UNIX command line.
    
    

"""

import sys

from gateway import SMSGateway

def main():
    """ """
    username = sys.argv[1]
    api_key = sys.argv[2]
    number = sys.argv[3]
    
    content = sys.argv[4]
    
    gateway = SMSGateway(username, api_key)
    
    id = gateway.generate_id()
    
    gateway.send_sms(id, int(number), unicode(content))
    
            
if __name__ == "__main__":
    main()