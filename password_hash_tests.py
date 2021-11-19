import requests
import json # necessary as using {'some': 'data'} directly in the data= results in a Malformed Input message
# TODO integrate behave or pytest-bdd for better reporting etc


# global data
password_hash_url = 'http://127.0.0.1:8088'
hash_endpoint = '/hash'
stats_endpoint = '/stats'
#headers = {"Content-Type": "application/json"} #not necessary but initially thought its lack may have been causing error with this script
good_password1 = {"password": "testpassword"} # good_password is defined as having "password" as the key, otherwise error happens. See github issue
successful_hash_counter = 0
upper_bound_hash_compute_ms = 6000 # since it waits 5 seconds give it another 1000ms
password_prefix1 = 'furious_simian'
password_prefix2 = 'upset_orangutan'
password_prefix3 = 'nonplussed_lemur'

""" Script testing stuff left in to show process to get this script working with the password hash program.
 It took a bit of time to narrow down where the Malformed Input error was originating from, it was easy to
 determine that passing the variable url to the post function was ok, but the password object took longer to
 figure out, eventually leading to the the use of json.dumps()
"""
#x = requests.post('http://127.0.0.1:8088/hash', headers=headers, data=good_password_obj) # Malformed Input message on cmd window
#x = requests.post(url, data=json.dumps({'password': 'testpassword'}), headers=headers) # finally works, headers param not actually needed
#x = requests.post('http://127.0.0.1:8088/hash', data='shutdown') # works, so url string isn't causing Malformed Input message
#r = requests.get('https://api.github.com/events') # works, shows single quote issue with windows curl isn't affecting the requests library
#r = requests.get('http://127.0.0.1:8088/hash/1') # works
# print(x.text)
#print(r.text)
#r = requests.post('https://httpbin.org/post', data={'key': 'value'})

"""
Returns the job identifier since this is used on other tests. The /stats TotalRequests includes bad requests, this cant reliably be used for this purpose
"""


# -------------password hash functions------------
def password_hash(endpoint, password_json):  # returns job identity
    response = requests.post(endpoint, data=json.dumps(password_json))
#    print("Status Code: " + response.status_code)
    print("Job #: " + response.text)
    return response.text


def get_generated_passwordhash(endpoint, jobident):  # takes job# and returns the generated pw hash
    # print('built endpoint: ' + endpoint + hash_endpoint + '/' + str(jobident))
    response = requests.get(endpoint + hash_endpoint + '/' + str(jobident))
    # print('built endpoint: ' + endpoint + hash_endpoint + '/' + '1')
    # response = requests.get(endpoint + hash_endpoint + '/' + '1')
    # print(response.text)
    return response.text


def password_stats(endpoint):
    response = requests.post(endpoint + stats_endpoint)
    return response


def password_shutdown(endpoint):
    response = requests.post(endpoint, data='shutdown')
    print("Shutdown response: " + response.text)
    print("Shutdown status: " + str(response.status_code))
    return response.status_code


def build_json_password(password):
    json_password = {'password': password}
    return json_password


# ----------------------Tests---------------------
# Main success scenario
def test_01_successful_password_hash(endpoint, password):
    response = password_hash(endpoint + hash_endpoint, password)
    testpassed = False
    if isinstance(int(response), int):
        testpassed = True
    print('test_01_successful_password_hash passed: ' + str(testpassed))


# tests that 2 different passwords resolve to different hashes
def test_02_password_hash_resolves_different_passwords_to_different_values(endpoint, password1, password2):
    jobidentifier1 = password_hash(endpoint + hash_endpoint, build_json_password(password1))
    jobidentifier2 = password_hash(endpoint + hash_endpoint, build_json_password(password2))
    passwordhash1 = get_generated_passwordhash(endpoint, jobidentifier1)
    passwordhash2 = get_generated_passwordhash(endpoint, jobidentifier2)
    testpassed = False
    if passwordhash1 != passwordhash2:
        testpassed = True
    print('test_02_password_hash_resolves_different_passwords_to_different_values : ' + str(testpassed))


def test_03_same_password_resolves_to_same_hash_value(endpoint, password):
    jobidentifier1 = password_hash(endpoint + hash_endpoint, build_json_password(password))
    jobidentifier2 = password_hash(endpoint + hash_endpoint, build_json_password(password))
    passwordhash1 = get_generated_passwordhash(endpoint, jobidentifier1)
    passwordhash2 = get_generated_passwordhash(endpoint, jobidentifier2)
    testpassed = False
    if passwordhash1 == passwordhash2:
        testpassed = True
    print('test_03_same_password_hash_resolves_to_same_value : ' + str(testpassed))


def test_04_endpoint_stats_test(endpoint):
    # first find out where we are on the job#
    response = password_stats(endpoint)
    # print('test_02_endpoint_stats_test # of requests: ' + response.text)
    # print('test_02_endpoint_stats_test # of requests: ' + str(response.json()))
    # print('test_02_endpoint_stats_test raw response: ' + str(response))
    # print('test_02_endpoint_stats_test status code: ' + str(response.status_code))
    stats = response.json()
    # test that the TotalRequests stats is incremented by invoking the hash after recording initial job#
    initialrequests = stats['TotalRequests']
    password_hash(endpoint + hash_endpoint, good_password1) #to increment total requests
    newresponse = password_stats(endpoint)
    newstats = newresponse.json()  # could just reuse stats here but trying to make it explicit what is going on
    newtotalrequests = newstats['TotalRequests']
    testpassed = False
    if newtotalrequests - 1 == initialrequests:  # this will likely fail if multiple simultaneous testers on pw hash
        testpassed = True
    print('test_04_endpoint_stats_test Total Requests incremented correctly : ' + str(testpassed))

    # test that the average time reported is reasonable (should be under the response time max as an upper bound):
    testpassed = False
    if stats['AverageTime'] < upper_bound_hash_compute_ms:
        testpassed = True
    print('test_04_endpoint_stats_test Average Time is reasonable: ' + str(testpassed))


# def test_xx_test_password_is_base64_encoded
# [A-Z, a-z, 0-9, and + /] + padded with = to make 64 digits


#def test_05_concurrency_test(endpoint):
# use threading module here

def test_06_shutdown_test(endpoint):
    response = password_shutdown(endpoint + hash_endpoint)
    testpassed = False
    if response == 200:
        testpassed = True
    print('test_06_shutdown_test responded with status 200: ' + str(testpassed))



""" Test Runner Section  """
# Test Data
test_02_password1 = password_prefix1 + str(successful_hash_counter)
#print("test2 pw1 " + test_02_password1)
test_02_password2 = password_prefix2 + str(successful_hash_counter)
#print("test2 pw2 " + test_02_password1)
test_03_password = password_prefix3 + str(successful_hash_counter)


test_01_successful_password_hash(password_hash_url, good_password1)
test_02_password_hash_resolves_different_passwords_to_different_values(password_hash_url, test_02_password1, test_02_password2)
test_03_same_password_resolves_to_same_hash_value(password_hash_url, test_03_password)
test_04_endpoint_stats_test(password_hash_url)
test_06_shutdown_test(password_hash_url)





