import os
import json
import requests


def get_next_url(response):
    link = response.headers['link']
    if link is None:
        return None

    links = link.split(',')
    for link in links:
        if 'rel="next"' in link:
            return link[link.find('<') + 1:link.find('>')]

    return None


def get_items(token, user_name):
    url = 'https://qiita.com/api/v2/users/{}/stocks'.format(user_name)
    headers = {'Authorization': 'Bearer {}'.format(token)}

    items = []
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        items.extend(json.loads(response.text))
        url = get_next_url(response)
        if url is None:
            break

    return items


def delete_item(token, item_id):
    url = 'https://qiita.com/api/v2/items/{}/stock'.format(item_id)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.delete(url, headers=headers)


def main():
    token = os.environ['QIITA_TOKEN']
    user_name = os.environ['USER_NAME']
    items = get_items(token, user_name)

    for item in items:
        delete_item(token, item['id'])


if __name__ == '__main__':
    main()
