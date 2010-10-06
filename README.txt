Introduction
============

``mfabrik.sms`` package allows send and receive SMS messages through mFabrik's SMS gateway.
This package provides Python bindings for HTTP API. The API can be purchased as a service
and requires an API key.

Usage
-----


Example::


	from mfabrik.sms import SMSGateway
			
	gateway = SMSGateway(client = os.environ["SMS_USERNAME"], api_key = os.environ["SMS_APIKEY"])

	# Do not store crendentials with source code, but read them from OS environment variables
	gateway.send(
	

