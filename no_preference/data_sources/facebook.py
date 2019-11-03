import pandas as pd
import time


def post():
    a = pd.read_json("../../datasets/your_posts_1.json")
    for x in a['posts']:
        if 'data' in x:
            for y in x['data']:
                if 'post' in y:
                    # post with user comments
                    # print(y['post'])
                    # timestamp in original format
                    # print(x['timestamp'])
                    # timestamp in readable format (Day Month Date hh:mm:ss year)
                    # print(time.ctime(x['timestamp']))
                    # print(pd.to_datetime(x['timestamp']).date())

                    data = {'Post': [y['post']], 'Time': [time.ctime(x['timestamp'])]}
                    df = pd.DataFrame(data)
                    print(df[['Post', 'Time']])
    return


def friends():
    b = pd.read_json("../../datasets/friends.json")
    for x in b['friends']:
        data = {'Name': x['name'], 'Time': [time.ctime(x['timestamp'])]}
        df = pd.DataFrame(data)
        print(df[['Name', 'Time']])
    return


def likepages():
    c = pd.read_json("../../datasets/pages.json")
    for x in c['page_likes']:
        data = {'Name': x['name'], 'Time': [time.ctime(x['timestamp'])]}
        df = pd.DataFrame(data)
        print(df[['Name', 'Time']])
    return


def search():
    d = pd.read_json("../../datasets/your_search_history.json")
    for x in d['searches']:
        if 'data' in x:
            for y in x['data']:
                if 'text' in y:
                    data = {'Text': [y['text']], 'Time': [time.ctime(x['timestamp'])]}
                    df = pd.DataFrame(data)
                    print(df[['Text', 'Time']])
    return


def functions():
    print("==========POSTS==========")
    post()
    print("==========FRIENDS==========")
    friends()
    print("==========LIKE PAGES==========")
    likepages()
    print("==========SEARCHES==========")
    search()


if __name__ == "__main__":
    functions()
