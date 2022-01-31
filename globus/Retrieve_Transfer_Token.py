#!/usr/bin/env python
import globus_sdk

# you must have a client ID
CLIENT_ID = 'ffef7b3d-8590-48d5-b732-021a58e85183'

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow()

authorize_url = client.oauth2_get_authorize_url()
print('Please go to this URL and login: {0}'.format(authorize_url))

# or just input() on python3
auth_code = input(
    'Please enter the code you get after login here: ').strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

# the useful values that you want at the end of this
globus_auth_data = token_response.by_resource_server['auth.globus.org']
globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
globus_auth_token = globus_auth_data['access_token']
globus_transfer_token = globus_transfer_data['access_token']

f=open('globus_auth_token.txt','w')
f.write(globus_auth_token)
f.close()

f=open('globus_transfer_token.txt','w')
f.write(globus_transfer_token)
f.close()
