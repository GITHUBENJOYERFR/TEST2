import requests
from bs4 import BeautifulSoup
import requests

contacts = 'Отдел продаж : +77000000000 \n' \
           'Отдел контроль качества: +77000000001 \n' \
           'Тех отдел: +77000000002 \n' \
           'Отдел маркетинга: +77000000003'

def parser(city,dates1,dates2):
    Headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

    url = f'https://www.booking.com/searchresults.html?ss={city}' \
          f'&dest_type=city&checkin={dates1}&checkout={dates2}&group_adults=1&no_rooms=1' \
          f'&group_children=0'

    req = requests.get(url,headers=Headers)

    with open('index.html','w',encoding='utf-8') as file:
        print('запись шаблона')
        file.write(req.text)

    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content,'html.parser')
    names_hotel = soup.findAll(class_='f6431b446c a15b38c233')
    prices = soup.findAll(class_='f6431b446c fbfd7c1165 e84eb96b1f')
    otzivs = soup.findall(class_='a3b8729ab1 d86cee9b25')
    uslovies = soup.findAll(class_='ccbf515d6e c07a747311')
    lst = []
    for numb in range(len(names_hotel)):
        new = []
        name = names_hotel[numb].text
        print(name)
        price = prices[numb].text
        print(price)
        otziv = otzivs[numb].text
        print(otziv)
        uslovie = uslovies[numb].text
        print(uslovie)
        new.append(uslovie)
        new.append(otziv)
        new.append(name)
        new.append(price)
        print(new)
        lst.append(new)
    return lst
