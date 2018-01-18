from bs4 import BeautifulSoup
import requests,os
import re

link = 'https://feedback.aliexpress.com/display/productEvaluation.htm?productId=32575976192&ownerMemberId=223191960'
link = 'https://feedback.aliexpress.com/display/productEvaluation.htm?productId=32658207253&ownerMemberId=220564633'
#link = 'https://feedback.aliexpress.com/display/productEvaluation.htm?productId=32765406931&ownerMemberId=228477332'


html_page = requests.get(link)
soup = BeautifulSoup(html_page.text, 'html.parser')


link = 'https://feedback.aliexpress.com/display/productEvaluation.htm#feedback-list'

ownerMemberId = '220564633'
productId = '32658207253'


cur_page = 1
while True:
    payload = {'ownerMemberId': ownerMemberId,
               'productId': productId,
               'page': cur_page,
               'withPictures': 'true'}
    page = requests.post(link, data=payload)
    soup = BeautifulSoup(page.text, 'html.parser')
    #print (soup)
    feedback_items = soup.find_all('dl', class_='buyer-review')
    if len(feedback_items)<1: break
    for fi in feedback_items:
        print('------------------')
        fi_date = fi.find('dd', class_='r-time')
        print(re.sub(r"\s+", u"_", fi_date.get_text()).replace(':','-'))
        fi_images = fi.find_all('img')
        for img in fi_images:
            print (img.get('src'))


        #print(fi)
    cur_page = cur_page+1

    #
    # if not os.path.exists('.\\'+productId):
    #     os.mkdir('.\\'+productId)
    #
    #
    # if len(images)>0:
    #     cur_page = cur_page+1
    #     cnt = 1
    #     for img in images:
    #
    #         file = requests.get(img.get('src'))
    #         print(img.get('src'))
    #         with open('.\\'+productId+'\\' + str(productId) + '_' + str(cnt) + '.jpg', 'wb') as f:
    #             f.write(file.content)
    #         cnt = cnt + 1
    #     else:
    #         break

