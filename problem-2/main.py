import socket,click
import json,time    
from numpy import mean, median
import urllib.parse as urlparse
import os
import validators,sys


def url_validation(url):
    """[Validates the URL]

    Args:
        url ([string]): [eg: https://worker.saihitesh98.workers.dev]

    Returns:
        [Boolean]: [True, if URL is okay.]
    """
    if not validators.url(url):
        print("Not a valid url. Please try again with proper URL structure.")
        return False
    else: 
        return True

def socket_connection_url(url):
    """[Convertion to a valid socket URL]

    Args:
        url ([string]): [eg: https://worker.saihitesh98.workers.dev]

    Returns:
        [string]: [worker.saihitesh98.workers.dev]
    """
    url = url.replace("http://","")
    url = url.replace("https://","")
    url = url.replace("www.", "")
    path=url.partition("/")[-1]
    tranformed_url=url.partition("/")[0]
    return path,tranformed_url

def status_code(data):
    res = [int(i) for i in data.decode('utf-8').split() if i.isdigit()] 
    status=res[0]
    return status
    

def socket_connection(url):
    """[Creates a socket connection]

    Args:
        url ([string]): [eg: https://worker.saihitesh98.workers.dev]

    Returns:
        [bytes]: [Returns data in bytes after establishment of socket connection]
    """

    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Arguments: socket.AF_INET => IPv4, socket.SOCK_STREAM => TCP
        # print("Socket successfully created")
    except socket.error as err: 
        print("socket creation failed with error %s" %(err))
    path,transformed_url=socket_connection_url(url)
    try: 
        host_ip = socket.gethostbyname(transformed_url)
    except socket.gaierror: 
        # this means could not resolve the host 
        print("there was an error resolving the host")
        sys.exit()
    s.connect((host_ip, 80))
    b=bytes("GET /"+path+" HTTP/1.0\r\nHost:"+transformed_url+"\r\n\r\n", 'utf-8')
    s.sendall(b)
    data=s.recv(2048)
    s.close()
    # print("Socket closed")
    return data

def metrics(url,profile):
    """[Display metrics]

    Args:
        url ([string]): [eg: https://worker.saihitesh98.workers.dev]
        profile ([integer]): [no of requests to calculate metrics]
    """    
    status_of_the_request=[]
    size_of_the_response=[]
    error_codes=[]
    success_count=0
    duration=[]
    i=1
    while(i<=int(profile)):
        start = time.perf_counter()
        data=socket_connection(url)
        duration.append(time.perf_counter()-start)
        status=status_code(data)
        size_of_the_response.append(len(data))
        status_of_the_request.append(status)
        i+=1
    for i in range(len(status_of_the_request)):
        if status_of_the_request[i]!=200:
            error_codes.append(status_of_the_request[i])
        else:
            success_count+=1
    print("The number of requests: ", profile)
    print("Error codes are: ", error_codes)
    print("Success Count: ", success_count)
    print("The fastest time: ", min(duration), "s")
    print("The slowest time: ", max(duration),"s")
    print("The mean time: ", mean(duration), "s")
    print("The median time: ", median(duration), "s")
    print("Success percentage is : ", str((success_count/len(status_of_the_request))*100))
    print("The size in bytes of the smallest response : ", min(size_of_the_response))
    print("The size in bytes of the largest response: ", max(size_of_the_response))



@click.command()
@click.option('--url','-u', type=str, help='worker site URL', nargs=1, required=True)
@click.option('--profile','-p', type=int, help='no of requests', nargs=1)
def main(url,profile):
    if (url_validation(url)):
        if profile:
            metrics(url,profile) #if profile arrgument is passed metrics are displayed
        else:
            data=socket_connection(url)
            path,transformed_url=socket_connection_url(url)
            if "links" in path:
                #links added in url path, JSON is displayed
                print(json.loads(data.decode("utf-8").split("\n")[-1])) 
            else: 
                #default
                print(data.decode("utf-8"))
     

if __name__ == '__main__':
    main()
