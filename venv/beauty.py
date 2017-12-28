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
                    'Platform': platform, 'Total Supply': total_supply, 'Twitter Count': twitter_count,
                    'FB Count': fb_count, 'Twitter Handle': twitter_handle
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
twitter_count = []
fb_count = []
twitter_handle = []
_access_token = 'EAACEdEose0cBAFVlII3WHaV4hGnnXeRmP2W8DtRavDP3vMcgQml06ZAX5Ik5FPY9m8Lra50xkIHGZAPPQpBDZBSQEpni7wJfl8TqbwrLDkcwI65OedMbZCB43y0jjb2qfvW9UgKGjjZAuct6QaoEUa72et2qJ4Ct2NZBj0eSdAIB1EU3tPQhBjsphqFI82LZBvdHjSp1JnaeQZDZD'


def getDataFromLinks(name_link_map):
    for name, link in name_link_map.iteritems():
        try:
            print link
            r = requests.get(link)
            _name.append(name)
            _link.append(link)
            data = r.text
            soup = BeautifulSoup(data, 'lxml')
            detail = {'project': '', 'platform': '', 'category': '', 'supply': '', 'start': '', 'end': '',
                      'twitter_count': '', 'twitter_handle': '', 'fb_count': ''}
            for x in soup.findAll("div", {"class": "infoitem"}):
                if 'Project Type' in x.text:
                    detail['project'] = x.text.replace('Project Type', '')
                elif 'Platform' in x.text:
                    detail['platform'] = x.text.replace('Platform', '')
                elif 'Category' in x.text:
                    detail['category'] = x.text.replace('Category', '')
                elif 'Total Supply' in x.text:
                    detail['supply'] = x.text.replace('Total Supply', '')
                elif 'Start Date' in x.text:
                    detail['start'] = x.text.replace('Start Date', '').replace('- -Days- -Hours- -Mins- -Secs', '')
                elif 'End Date' in x.text:
                    detail['end'] = x.text.replace('End Date', '').replace('- -Days- -Hours- -Mins- -Secs', '')
                elif 'WebsiteOpen' in x.text:
                    web_link = x.find('a', attrs={'href': re.compile("^https://")})
                    if web_link:
                        h = web_link.get('href')
                        print 'web_link ' + str(h)
                        data = requests.get(h, verify=False)
                        if data.text.find('twitter.com') > 0:
                            html = data.text
                        else:
                            browser = webdriver.PhantomJS()
                            browser.get(h)
                            html = browser.page_source
                        s = BeautifulSoup(html, 'lxml')
                        twitter_link = s.find('a', attrs={'href': re.compile("twitter\.com")})
                        fb_link = s.find('a', attrs={'href': re.compile("facebook\.com")})
                        if twitter_link:
                            h1 = twitter_link.get('href')
                            user_name = h1.split('/')[3]
                            detail['twitter_handle'] = user_name
                            twiter_json_link = 'https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names=' + user_name.replace(
                                '@', '')
                            json_obj = json.loads(requests.get(twiter_json_link).text)
                            if json_obj:
                                detail['twitter_count'] = str(json_obj[0][u'followers_count'])
                            else:
                                detail['twitter_count'] = ''
                        if fb_link:
                            _fb = fb_link.get('href')
                            fb_graph_url = "https://graph.facebook.com/v2.4/" + _fb.split('/')[
                                3] + "?fields=id,name,likes,link&access_token=" + _access_token
                            fb_json_obj = json.loads(requests.get(fb_graph_url).text)
                            if not fb_json_obj.get('error', ''):
                                detail['fb_count'] = str(fb_json_obj[u'likes'])
                            else:
                                detail['fb_count'] = ''

            project.append(detail['project'])
            platform.append(detail['platform'])
            category.append(detail['category'])
            total_supply.append(detail['supply'])
            start_date.append(detail['start'])
            end_date.append(detail['end'])
            twitter_count.append(detail['twitter_count'])
            fb_count.append(detail['fb_count'])
            twitter_handle.append(detail['twitter_handle'])
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
