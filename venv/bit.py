import requests
from pandas import DataFrame


def start():
    url = 'https://api.icowatchlist.com/public/v1/'
    response = requests.get(url)
    json_res = response.json()
    name =[]
    image=[]
    icowatchlist_url =[]
    end_time=[]
    timezone=[]
    start_time=[]
    website_link =[]
    description=[]
    count = 0
    for i in json_res['ico']['live']:
        if count <11:
            name.append(i['name'])
            image.append(i['image'])
            icowatchlist_url.append(i['icowatchlist_url'])
            end_time.append(i['end_time'])
            timezone.append(i['timezone'])
            start_time.append(i['start_time'])
            website_link.append(i['website_link'])
            description.append(i['description'])
            count +=1
        else:
            break

    df = DataFrame({'Name': name, 'Image': image, 'icowatchlist URL': icowatchlist_url, 'End Time': end_time, 'Start Time': start_time,
                    'Website Link':website_link, 'Description':description
                    })

    df.to_excel('test.xlsx', sheet_name='sheet1', index=False)







if __name__=='__main__':
    start()
