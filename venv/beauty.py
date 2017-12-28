from bs4 import BeautifulSoup
import requests
from pandas import DataFrame
import json
import logging
import re
from selenium import webdriver

def export():
    df = DataFrame({'Name': _name, 'Link': _link, 'Project Type': project,
                    'End Date': end_date, 'Start Date': start_date, 'Category': category,
                    'Platform': platform, 'Total Supply': total_supply, 'Twitter Count':followers_count
                    })

    df.to_excel('bit.xlsx', sheet_name='sheet1', index=False)


_name = []
_link = []
project = []
platform = []
category = []
total_supply = []
end_date = []
start_date = []
followers_count =[]

def getDataFromLinks(name_link_map):
    for name, link in name_link_map.iteritems():
        try:
            print link
            r = requests.get(link)
            _name.append(name)
            _link.append(link)
            data = r.text
            soup = BeautifulSoup(data, 'lxml')
            detail = {'project': '', 'platform': '', 'category': '', 'supply': '', 'start': '', 'end': '','followers_count': ''}
            for x in soup.findAll("div", {"class": "infoitem"}):
                if 'Project Type' in x.text:
                    detail['project'] = x.text.replace('Project Type', '')
                if 'Platform' in x.text:
                    detail['platform'] = x.text.replace('Platform', '')
                if 'Category' in x.text:
                    detail['category'] = x.text.replace('Category', '')
                if 'Total Supply' in x.text:
                    detail['supply'] = x.text.replace('Total Supply', '')
                if 'Start Date' in x.text:
                    detail['start'] = x.text.replace('Start Date', '').replace('- -Days- -Hours- -Mins- -Secs', '')
                if 'End Date' in x.text:
                    detail['end'] = x.text.replace('End Date', '').replace('- -Days- -Hours- -Mins- -Secs', '')
                if 'Website' in x.text:
                    web_link = x.find_all('a', attrs={'href': re.compile("^https://")})
                    flag=False
                    if web_link:
                        h = web_link[0].get('href')
                        print 'web_link ' + str(h)
                        browser = webdriver.PhantomJS('C:\Users\Harit\Downloads\phantomjs-2.1.1-windows\bin\phantomjs')
                        browser.get(h)
                        html = browser.page_source
                        s = BeautifulSoup(html, 'lxml')
                        twitter_link = s.find_all('a', attrs={'href': re.compile("twitter\.com")})
                        if twitter_link:
                            h1= twitter_link[0].get('href')
                            print 'twitter_link ' + str(h1.split('/'))
                            user_name = h1.replace('https://www.twitter.com/','')
                            print 'user_name ' + user_name
                            twiter_json_link = 'https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names='+user_name
                            json_obj = json.loads(requests.get(twiter_json_link).text)
                            print 'json_obj ' + str(json_obj)
                            flag = True
                    if flag and json_obj:
                        detail['followers_count'] = str(json_obj[0][u'followers_count'])
                        print 'followers_count ' + str(followers_count)
                    else:
                        detail['followers_count'] =''






            project.append(detail['project'])
            platform.append(detail['platform'])
            category.append(detail['category'])
            total_supply.append(detail['supply'])
            start_date.append(detail['start'])
            end_date.append(detail['end'])
            followers_count.append(detail['followers_count'])
        except Exception as e:
            print 'EXCEPTION ' + str(link)
            logging.exception("message")
            pass
    print 'Crawling the child links Done!!'


def start():
    url = "https://www.coinschedule.com/"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    name_link_map = {}
    print 'Start crawling....'
    for link in soup.findAll("div", {"class": "upcoming list-table"}):
        for td in link.find_all('td'):
            for a in td.find_all('a'):
                name_link_map[a.text] = a.get('href')
    print 'Start crawling the child links....'
    getDataFromLinks(name_link_map)
    export()
    print 'Sheet has been created!!!'


if __name__ == '__main__':
    start()


