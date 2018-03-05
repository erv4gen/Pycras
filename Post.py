import traceback

from bs4 import BeautifulSoup
import urllib
from urllib.error import URLError

import time
import random
import re
from datetime import datetime, timedelta

from selenium.common.exceptions import NoSuchElementException


class Post(object):

    def __init__(self, url, location, category, title='', content='', email='', date='', status=0, driver=''):

        self.url = url
        self.location = location
        self.category = category
        self.title = title
        self.content = content
        self.email = email
        self.date = date
        self.status = status
        self.driver = driver
        self.get_post()


    def get_post(self):

        # print(self.url)
        try:

            def get_h():
                headers = {

                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
                return  headers

            req = urllib.request.Request(
                self.url,
                data=None,
                headers= get_h()
            )

            soup = BeautifulSoup(urllib.request.urlopen(req).read().decode('utf-8'), "html5lib")
            time.sleep(10)



            self.title = soup.title.string

            # get the content of the post
            post_content = soup.find('section', {'id':'postingbody'})  # section', {'id':'postingbody'}).text)
            # remove repetions of <br> and [/br] at the end of the post
            #post_content = re.sub(r'(<br>){2,}', '', post_content, flags=re.IGNORECASE)
            #post_content = re.sub(r'(</br>){2,}', '', post_content, flags=re.IGNORECASE)
            self.content = post_content.text

            # get the reply email for the post, the info that I need are in another html page
            reply = soup.find(id='replylink')  # 'a', {'id':'replylink'})
            if reply is not None:
                reply_link = reply['href']
                reply_url = self.url[:self.url.find('.org/') + 4] + reply_link

                #reply_page = BeautifulSoup(urlopen(reply_url).read(),"html5lib")
                #headers = get_h()
                #for key, value in enumerate(headers):
                  #  capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
                  #  webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = value

                p_element = None
                try:
                    time.sleep(10)
                    self.driver.get(reply_url)
                    p_element = self.driver.find_element_by_class_name('anonemail')

                except NoSuchElementException as e:
                    print("Fail with Capcha\n",e)
                except Exception as e:
                    print(e)
                #reply_page = BeautifulSoup(urlopen(reply_url).read(), "html5lib")
                #self.email = reply_page.find('div', class_='anonemail')#.string  # {'class':'anonemail'}).string
                if p_element is not None:
                    self.email = p_element.text
                    print("Post", self.url, " saved successfully")
                else:
                    self.email = '-'
            # self.email = format(reply_email)

        except URLError as error:
            print(error)
        except Exception as e:
            print(e)
    def get_location(self):
        return self.location

    def get_category(self):
        return self.category

    def get_catefory_full_name(self):
        return self.category_full_name

    def get_title(self):
        return self.title

    def get_body(self):
        return self.content

    def get_email(self):
        return self.email

    def get_date(self):
        return self.date

    def __str__(self):
        return 'Title:{title}. Date:{date}. Email:{email}. Location:{location}. Category:{category}'.format(
            title=self.title, date=self.date, email=self.email, location=self.location, category=self.category)
