from glob import glob
from os import path

import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp

from no_preference.lib.util import get_logger

LOGGER = get_logger(__name__)

_POSTS_COLUMNS = ['content', 'date']


def get_facebook_posts(facebook_data_dir: str):
    posts_files = glob(path.join(facebook_data_dir, 'your_posts_*.json'))

    posts_data = []
    for posts_file in posts_files:
        LOGGER.info(f'Getting posts from {posts_file}.')
        facebook_data = pd.read_json(posts_file)
        for i in range(len(facebook_data)):
            if type(facebook_data['data'][i]) is list:
                data = facebook_data['data'][i]
                posts = [d['post'] for d in data if 'post' in d]
                if len(posts) == 1:
                    post = posts[0]
                else:
                    continue
            timestamp: Timestamp = facebook_data['timestamp'][i]
            posts_data.append([post, timestamp])
    return pd.DataFrame(posts_data, columns=_POSTS_COLUMNS)


def functions():
    print("==========POSTS==========")
    posts = get_facebook_posts('charlyn_facebook')
    print(posts)


if __name__ == "__main__":
    functions()
