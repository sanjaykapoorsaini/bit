from bs4 import BeautifulSoup
import requests
from pandas import DataFrame

def export():
    df = DataFrame({'Name': _name, 'Link': _link, 'Project Type': project,
                    'End Date': end_date, 'Start Date': start_date, 'Category': category,
                    'Platform': platform, 'Total Supply':total_supply,
                    })

    df.to_excel('bit.xlsx', sheet_name='sheet1', index=False)


_name =[]
_link =[]
project =[]
platform =[]
category= []
total_supply =[]
end_date=[]
start_date=[]
def getDataFromLinks(name_link_map):
    for name, link in name_link_map.iteritems():
        try:
            r = requests.get(link)
            _name.append(name)
            _link.append(link)
            data = r.text
            soup = BeautifulSoup(data, 'lxml')
            detail = {'project':'','platform':'','category':'', 'supply':'','start':'','end':'',}
            for x in soup.findAll("div", { "class" : "infoitem" }):
                if 'Project Type' in x.text:
                    detail['project'] = x.text.replace('Project Type','')
                if 'Platform' in x.text:
                    detail['platform'] = x.text.replace('Platform','')
                if 'Category' in x.text:
                    detail['category'] =x.text.replace('Category','')
                if 'Total Supply' in x.text:
                    detail['supply'] = x.text.replace('Total Supply','')
                if 'Start Date' in x.text:
                    detail['start']=x.text.replace('Start Date','').replace('- -Days- -Hours- -Mins- -Secs','')
                if 'End Date' in x.text:
                    detail['end'] =x.text.replace('End Date','').replace('- -Days- -Hours- -Mins- -Secs','')
            project.append(detail['project'])
            platform.append(detail['platform'])
            category.append(detail['category'])
            total_supply.append(detail['supply'])
            start_date.append(detail['start'])
            end_date.append(detail['end'])
        except:
            print 'EXCEPTION ' + str(link)
            pass
    print 'Crawling the child links Done!!'

def start():
    url = "https://www.coinschedule.com/"
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    name_link_map = {}
    print 'Start crawling....'
    for link in soup.findAll("div", { "class" : "upcoming list-table" }):
        for td in link.find_all('td'):
            for a in td.find_all('a'):
                name_link_map[a.text] = a.get('href')
    print 'Start crawling the child links....'
    getDataFromLinks(name_link_map)
    export()
    print 'Sheet has been created!!!'

if __name__=='__main__':
    start()

