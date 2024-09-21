from utils import download
import time


def redirect_resp(resp, config):
    # Redirect to a page if http status is within 300 range
    # If redirection dig too deep, it wont excavate
    
    redirect_url = resp.raw_response.headers["location"]
    depth = 3
    while True:
        new_resp = download.download(redirect_url, config)

        if 300 <= new_resp.status < 400 and depth > 0:
            redirect_url = new_resp.raw_response.headers["location"]
            time.sleep(config.time_delay)   # Ensure politeness during redirection
            depth -= 1
            continue
        else:
            if new_resp.status == 200:
                return new_resp
            else:
                break

    print("INFO - Redirect failed")
    return None
