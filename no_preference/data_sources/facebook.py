import pandas as pd
import time

from math import isnan


def post():
    a = pd.read_json("../../datasets/your_posts_1.json", convert_dates=False)
    posts_data = []
    for i in range(len(a)):
        if type(a['data'][i]) is list:
            data = a['data'][i]
            posts = [d['post'] for d in data if 'post' in d]
            if (len(posts) == 1):
                post = posts[0]
            else:
                continue
        timestamp = a['timestamp'][i]
        posts_data.append([post, timestamp])
    return pd.DataFrame(posts_data, columns=['post', 'timestamp'])


def functions():
    print("==========POSTS==========")
    print(post())


if __name__ == "__main__":
    functions()
