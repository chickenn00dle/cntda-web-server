# HTTP Functions Module
#######################

# Imports
import re
import os
import datetime

# Functions
'''
Primary handle function
Get request header, check method and path, and create response accordingly
'''
def http_handle(request_string):
    assert not isinstance(request_string, bytes)
    req_header = http_get_header(request_string)
    path = req_header.get('GET')[0]
    status = 200
    if not http_is_get(req_header):
        status = 403
    if not http_is_valid_path(path):
        status = 404
    res_header = http_create_res_header(status)
    if status > 200:
        return res_header
    res_body = http_create_res_body(path)
    response = res_header + '\n'
    response += res_body
    return response


'''
Parse request to create name/value header object
'''
def http_get_header(request):
    request_arr = request.splitlines()
    header = {}
    for line in request_arr:
        if len(line) > 0:
            header_arr = re.split('\s+|:\s', line)
            header[ header_arr[0] ] = header_arr[1:]
    return header


'''
Check method of request
True only if GET request
'''
def http_is_get(req_headers):
    return 'GET' in req_headers.keys()


'''
Confirm path is valid. 
True only if path is to file and file exists in data directory
'''
def http_is_valid_path(path):
    if not path:
        return False
    dir = re.search('^(.*/)', path)
    file = re.search('^.*/(\w+\.\w*)$', path)
    if not file:
        return False
    target = os.scandir('data/' + dir.group(1))
    for item in target:
        if not item.is_file():
            pass
        else:
            if item.name == file.group(1):
                return True
    return False


'''
Craft response header. Status is OK only if GET request. Otherwise 403/404
Additionally adds Date, Server, and Content-Type headers where applicable

i.e.

HTTP/1.1 200 OK
Content-Type: text/html
Date: Wed, 10 Aug 2019 12:00:00
Server: Python/3.7.4
'''
def http_create_res_header(status):
    header = 'HTTP/1.1'
    if status == 403:
        header += ' 403 Forbidden\n'
    elif status == 404:
        header += ' 404 Not Found\n'
    else:
        header += ' 200 OK\n'
        header += 'Content-Type: text/html\n'
    date = datetime.datetime.now()
    header += 'Date: ' + date.strftime("%a, %d %b %Y %H:%M:%S %Z") + '\n'
    header += 'Server: Python/3.7.4\n'
    return header


'''
Fetch file data from within data directory and create response body (assumes valid path)
'''
def http_create_res_body(path):
    print(path)
    with open('data' + path, 'r') as file:
        return file.read()
