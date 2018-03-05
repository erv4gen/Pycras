import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import URLError
import re
from datetime import datetime, timedelta
from Post import Post
import time
import random
from selenium import webdriver

def get_globals():
    try:
        config = {}
        exec(open('config.conf').read(), config)
        locations = config['locations']
        categories = config['categories']
        # output = '{}.html'.format(datetime.now().strftime('%Y%m%d%H%M'))
        return (locations, categories)

    except Exception as e:
        raise


def filter_by_date(ad_date):
    # I just care about the new posts of today.
    return datetime.now().date() == datetime.strptime(ad_date, '%Y-%m-%d %H:%M').date()


def get_proxy():
    plist = ['50.234.205.212:80']
    return plist


def get_posts(location, category):
    posts = []

    def get_h():
        headers = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        return headers


    url = ('https://' + location + '.craigslist.org/search/' + category)
    try:
        #proxy_support = urllib.request.ProxyHandler({'http': get_proxy()})
        #opener = urllib.request.build_opener(proxy_support)
        #urllib.request.install_opener(opener)

        req = urllib.request.Request(
            url,
            data=None,
            headers= get_h()
                                )

        soup = BeautifulSoup(urllib.request.urlopen(req).read().decode('utf-8'), "html5lib")
        time.sleep(10)

    except URLError:
        print()
        raise

    # gets list of post ids
    ids = soup.find_all('li', class_='result-row')

    # remove nearby posts and old ones
    ids = [post for post in ids if filter_by_date(post.time['datetime'])]
    #ids = [post for post in ids if post.a['href'][0] == '/']
    #ids = [post.a['href'] for post in ids]
    print("Next posts been found:")
    driver = webdriver.Firefox(executable_path='c:\\Users\\15764\\Documents\\geckodriver\\geckodriver.exe')
    for post in ids:
       # print(post.a['href'])
        posts.append(Post(post.a['href'], location, category, date=post.time['datetime'],driver=driver))

    return posts


def make_html(locations, categories, posts):
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('scraper', 'template'))
    template = env.get_template('template.html')
    html_output = template.render(locations=locations, categories=categories, posts=posts)
    output_destination = '{}.html'.format(datetime.now().strftime('%Y%m%d_%H:%M'))

    with open(output_destination, 'wb') as output:
        output.write(bytes(html_output, 'UTF-8'))

def get_columns():
    col = ['url','title','content','category','location','email','date']
    return col

def save_to_csv(posts):

    df = pd.DataFrame(columns=get_columns())
    for post in posts:
        new_row = [post.url,post.title,post.content,post.category,post.location,post.email,post.date]
        df.append(pd.Series(new_row),ignore_index=True)
    today = datetime.now().strftime("%d_%m_%y") +".csv"
    try:
        df.to_csv(today, index=False)
    except:
        pass
def main():
    locations, categories = get_globals()
    posts = []

    for location in locations:
        for category in categories:
            posts.extend(get_posts(location, category))

        # make ouput
    save_to_csv(posts)
    make_html(locations, categories, posts)
    print('Posts found:{n_posts}. Done!'.format(n_posts=len(posts)))


if __name__ == '__main__':
    print("Starting working..")
    main()
# p = Post('51', 'asheville', 'sad')
# print(p)
