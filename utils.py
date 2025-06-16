import requests
def is_valid_image(url):
    try:
        response = requests.head(url, timeout=2)
        return response.status_code == 200 and 'image' in response.headers.get('Content-Type', '')
    except:
        return False