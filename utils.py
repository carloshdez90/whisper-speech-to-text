import requests


def get_image_from_url(url):
    r = requests.get(url, allow_redirects=True)
    filename = url.split('/')[-1]
    open(filename, 'wb').write(r.content)

    return filename
