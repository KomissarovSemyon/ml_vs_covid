import requests
from bs4 import BeautifulSoup
import pandas as pd


class Parser:

    def __init__(self):
        pass

    def get_html(self, url):
        r = requests.get(url)
        r.encoding = 'utf8'
        return r.text
    
    def cat_link(self, s):
        return s.split('/')[2]
    
    def read_bbc(self, soup):
        try:
            main_story_body = soup.find('div', class_="story-body__inner").find_all('p') #bbc
            main_story_body = [i.string if i.string else " " for i in main_story_body]
            return ' '.join(main_story_body)
        except AttributeError:
            try:
                main_story_body = soup.find('div', class_="story-body__introdation").find_all('p') #bbc
                main_story_body = [i.string if i.string else " " for i in main_story_body]
                return ' '.join(main_story_body)
            except:
                return None
        
    def read_cnn(self, soup):
        try:
            main_story_body = soup.find('div', class_="l-container").find_all('div') #cnn
            main_story_body = [i.string if i.string else " " for i in main_story_body]
            return ' '.join(main_story_body)
        except AttributeError:
            return None
        
    def read_fake(self, soup):
        try:
            main_story_body1 = soup.find('div', class_="entry-content clearfix").find_all('h2') #fake
            main_story_body1 = [i.string if i.string else " " for i in main_story_body1]
            main_story_body2 = soup.find('div', class_="entry-content clearfix").find_all('p') #fake
            main_story_body2 = [i.string if i.string else " " for i in main_story_body2]
            main_story_body3 = soup.find('div', class_="entry-content clearfix").find_all('blockquote') #fake
            main_story_body3 = [i.string if i.string else " " for i in main_story_body3]
            main_story_body1 = ' '.join(main_story_body1)
            main_story_body2 = ' '.join(main_story_body2)
            main_story_body3 = ' '.join(main_story_body3)
            return ' '.join([main_story_body1, main_story_body2, main_story_body3])
        except AttributeError:
            return None
        
    def read_news(self, s):
        html = self.get_html(s)
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find('title').string
        link = s
        information_agency = self.cat_link(link)
        text = None
        if information_agency == 'edition.cnn.com':
            text = self.read_cnn(soup)
        elif information_agency == 'www.bbc.co.uk':
            text = self.read_bbc(soup)
        elif information_agency == 'worldnewsdailyreport.com':
            text = self.read_fake(soup)
        data = {'title': title, 'text': text, 'link': link, 'information_agency': information_agency}
        return data
