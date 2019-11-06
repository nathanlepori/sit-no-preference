from os import PathLike, path

import pandas as pd
import time

from no_preference.util import get_data_dir

_POSTS_COLUMNS = ['content', 'date']


def get_facebook_posts(facebook_data_dir: str):
    facebook_data = pd.read_json(path.join(get_data_dir(), 'datasets', 'facebook_data', facebook_data_dir))
    posts_data = []
    for i in range(len(facebook_data)):
        if type(facebook_data['data'][i]) is list:
            data = facebook_data['data'][i]
            posts = [d['post'] for d in data if 'post' in d]
            if len(posts) == 1:
                post = posts[0]
            else:
                continue
        timestamp = facebook_data['timestamp'][i]
        posts_data.append([post, time.ctime(timestamp)])
    return pd.DataFrame(posts_data, columns=_POSTS_COLUMNS)


def functions():
    print("==========POSTS==========")
    posts = get_facebook_posts('charlyn_facebook')
    print(posts)


if __name__ == "__main__":
    functions()
