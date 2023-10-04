#!/usr/bin/env python

# or just input() on python3
jgi_url = input(
    'Please enter the URL you retrieved via email from JGI here: ').strip()

(base,parameters) = jgi_url.split('?')

f=open('origin.txt','w')
for parameter in parameters.split('&'):
	f.write(parameter+'\n')
