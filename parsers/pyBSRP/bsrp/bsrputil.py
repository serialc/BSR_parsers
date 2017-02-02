# BSRP utilities that simplify individual protocols

from datetime import datetime
import os, requests, time, stat, socket#, pytz

def robust_url_retrieval(parameters, method='GET', post_data='', stn='', tries=5, timeout=20):
    bssid = parameters['city']
    url = parameters['url']

    # stn will only be used as a string
    # only needed for naming error files using unique names
    stn = str(stn)

    # get the url!
    attempt_num = 1
    first_try = get_url(url, bssid, method, post_data, stn, attempt_num, tries, timeout)

    # if it failed to retrieve, pause then try again, while we still have 'tries' left.
    while not first_try and attempt_num < tries:
        attempt_num = attempt_num + 1
        # wait a tiny bit longer between each attempt
        time.sleep(10 + attempt_num)
        first_try = get_url(url, bssid, method, post_data, stn, attempt_num, tries, timeout)

    # Failed all attempts
    if not first_try:
        print("Robust retrieval failed for " + bssid + " station number " + str(stn))
        return False
    
    # Succeeded, return results
    return first_try

def get_url(url, city, method="GET", post_data='', stn='', attempt=0, tries = -1, timeout_secs=20):

    # prep request
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'}

    try:
        # make the retrieval call
        if method == "POST":
            res = requests.post(url, headers=headers, data=post_data, timeout=timeout_secs)
        if method == "GET":
            res = requests.get(url, headers=headers, timeout=timeout_secs)
        
        # need to read here as it can throw errors
        url_data = res.text

        # raise error if one exists
        res.raise_for_status()
    except (urllib3.URLError, urllib3.HTTPError) as e:
        print("Station retrieval for " + city + " failed to retrieve url: " + url)
        # failed, return False
        return False

    if url_data == "" or url_data == "False" or res.status_code != 200:
        # only print message if tries == -1 or tries == 5
        if tries == -1 or tries == attempt:
            # only print message if this is the last attempt, or not a 'robust' retrieval
            message = "Downloaded data for [" + city + "] during snapshot [" + date_time + "] but it is empty.\n DEBUG INFO\n" + \
                "code: " + str(res.status_code) + " " + \
                "data: " + str(res.text) + "\n" + \
                "url: " + url + "\n" + \
                "contents: " + url_data + "\n"
            print( message )
        
        # retrieval failed!
        return False

    # actually reading data hopefully
    return url_data

def multiprocess_data(data, method='get'):
    from multiprocessing import Pool
    import time
    
    try:
        # create a pool of 16 workers
        pool = Pool(processes = 16)

        # make calls for each item in stn_list
        # determine if we are using get/post
        if method == 'get':
            stns = pool.map(mp_get, data)
        if method == 'post':
            stns = pool.map(mp_post, data)
    finally:
        # close pool and release memory
        pool.close()
        pool.join()

        return stns

def mp_post(par):

    # assign parameters to local variables
    url, post_vars, stn_num = par

    pkg = {'city': city, 'url': url}

    # note we have added the station number to the data field for 'POST'ing
    retrieved_data = robust_url_retrieval( pkg, method='POST', post_data= (post_vars + str(stn_num)), stn=stn_num, tries=2 )

    if not retrieved_data:
        return False

    return retrieved_data

def mp_get(par):

    # assign parameters to local variables
    url, stn_num, bssid = par
    
    # note we have added the station number to the url here
    pkg = {'city': bssid, 'url': url + str(stn_num)}

    retrieved_data = robust_url_retrieval( pkg, method='GET', tries=2 )
    
    if not retrieved_data:
        return False

    return retrieved_data
