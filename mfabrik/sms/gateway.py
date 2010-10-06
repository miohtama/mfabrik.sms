"""

    Zoho CRM API bridge.

"""

__copyright__ = "2010 mFabrik Research Oy"
__author__ = "Mikko Ohtamaa <mikko@mfabrik.com>"
__license__ = "GPL"
__docformat__ = "Epytext"

import time
import urllib

from odict import odict

from utils import calculate_call_signature, get_random_id, stringify

class BadInputException(Exception):
    """ Python functions receive badly formatted parameters """
    
class SMSServiceException(Exception):
    """ Remote end decided the parameters you give are not good """
    

class SMSGateway(object):
    """ mFabrik SMS service Python wrapper.  
    
    """
        
    def __init__(self, client, api_key, server_url="http://sms.mfabrik.com/Outgoing"):
        """    
        @param client: username for mFabrik SMS service
        
        @param api_key: API key for mFabrik SMS service
        
        @param server_url: Service URL (if you want to override9
        
        """
        self.client = client
        self.api_key = api_key
        self.server_url = server_url
        
    def generate_id(self):
        """
        @return: Random number to be used as an id, unless id want to be specific 
        """
        return get_random_id()         
        
    def send_sms(self, id, to, content, sender=None, to_alias=None, udh=None, pid=None, notify=None, response=None, response_group=None, response_time=None, multiple_responses=None):
        """ Send SMS message.        
        
        @param id:    Message identifier, string 32 characters. This field identifies the message uniquely. In case server receives the same ID from the same client, it assumes that the latter request is a duplicate (and rejects the duplicate request). E.g. 123123123    
                
        @param sender: Sending number for the SMS. Either numeric (like short code) or alphanumeric value that appears as the sender of the message to the mobile user. Not used if a response is set    

        @param to:   Message recipient, integer. This field determines the recipient of the message (MSISDN), and must be given in its international format without the leading + sign    358501234567
            
        @param to_alias:    Alternative recipient number, integer. This fields may be used to specify an alternative telephone number of the receipient that may appear as the sending number of the potential response from the recipient. This field has meaning only for response routing.
                
        @param content:    Message contents. This fields contains the payload of the message. The value is a unicode string.

        @param udh:    Optional user data header. Value is given as a hexadecimal value. Example: a6

        @param: pid    Optional PID flag. Example: 65

        @param notify:  Notify address, ASCII string 250 characters. If the client wants to know the status of the outgoing SMS, it can order a notification by specifying the URL that will be called by the server when the delivery status of the SMS changes. See later how the delivery notification works.  http://www.client.com/deliverystatus

        @param response:    Response address, ASCII string 250 characters. If the client expects the end-user to respond to the outgoing SMS, the client can order the response message by specifying the URL that will be called the server when the response arrives. See later how the response mediation works.    http://www.client.com/incomingsms

        @param response_group:    Response number group to be used for the sending number, string 2 characters. Values are allocated by the server administrator.    fi

        @param response_time:    The maximum time the server will wait for a potential response to the outgoing SMS. If the response arrives after the maximum time has elapsed, the response will be rejected. The value is given as minutes, and can range between 1 and 40320 (four weeks)    60

        @param multiple_responses:    Enable multiple responses. Value can be either 1 (on) or 0 (off, default). If set on, the server will keep the response thread open until the response_time has elapsed, so that several responses can be recieved to the single outgoing SMS    1
        
        @return: Internal transaction id of the send action (int)
        """
        
        if type(content) != unicode:
            raise BadInputException("Message content must be unicode.")
                
        if multiple_responses is not None:
            if multiple_responses is True:
                multiple_responses= "1"
            elif multiple_responses is False:
                multiple_responses= "0"
            else:
                raise BadInputException("Funny multiple response.") 

        if type(to) != long:
            raise BadInputException("Recipient number must be international phone number without + prefix. Make sure you use Python 'long' type. Got:" + unicode(to))

        timestamp = time.time()

        # Construct RPC parameteres
        
        params = odict()
                 
        params["client"] = self.client
        
        params["id"] = id

        if sender is not None:
            params["from"] = sender

        params["to"] = to
        
        if to_alias:
            params["to_alias"] = to_alias

        params["time"] = timestamp            
            
        params["content"] = content.encode("utf-8")

        if udh is not None:
            params["udh"] = pid
            
        if pid is not None:
            params["pid"] = pid

        if notify is not None:
            params["notify"] = notify

        if response_group is not None:
            params["response_group"] = response_group

        if response_time is not None:
            params["response_time"] = response_time

        if multiple_responses is not None:
            params["multiple_responses"] = self.api_key
            
        params["SSK"] = self.api_key
        
        stringify(params)
                        
        params["mac"] = calculate_call_signature(params)
            
        f = urllib.urlopen(self.server_url, urllib.urlencode(params))
        response = f.read()
        f.close()
        
        return self.handle_response(response)
        
    def handle_response(self, resp):
        """
        
        Response can be like:
        
            21 Invalid mac

        or:
            
            1234
        
        """
        
        parts = resp.split(" ")
        number = parts[0]
        
        try:
            response_code = int(number)
        except:
            raise SMSServiceException("Bad SMS service response body:" + resp)
        
        if response_code <= 21:
            raise SMSServiceException("Message send failed: " + resp)
            
        return number