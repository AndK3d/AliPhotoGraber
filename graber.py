from bs4 import BeautifulSoup
import requests
import re,os, time


category_page = 'https://ru.aliexpress.com/af/category/202032003.html'
category_page = 'https://ru.aliexpress.com/category/202002389/bras.html'
category_page = 'https://ru.aliexpress.com/category/202005131/stockings.html'

proxies = {
  'http': 'http://67.78.143.182:8080',
  'https': 'http://67.78.143.182:8080',
}

### Collect all items links from all pages in category in links[] list###

links = []
page_num=1
while True: # pages loop
    page_num_str = '?page=' + str(page_num)
    html_doc = requests.get(category_page+page_num_str, proxies = proxies)
    print (html_doc)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    page_items_links = soup.find_all(href=re.compile("item"), class_='picRind ')
    if len(page_items_links)>0: # if no more items on page - break loop
        for link in page_items_links:
            #print(link['href'])
            links.append('https:'+link['href'])
        print('page_num=',page_num)
        print('items count =',len(page_items_links))
        page_num = page_num + 1
        time.sleep(3)
    else:
        break

feedbacks_pages = []

for item in links: # items loop
    print('Current item:',item)
    html_page = requests.get(item)
    print (html_page)
    soup = BeautifulSoup(html_page.text, 'html.parser')
    for i in soup.find_all(thesrc=re.compile("productEvaluation")):
        string = str(i)
        owner = re.findall(r'ownerMemberId=\d+', string)
        product = re.findall(r'productId=\d+', string)
        ownerMemberId = owner[0].split('=')[1]
        productId = product[0].split('=')[1]

        cur_page = 1
        while True: #feedbacks pages loop
            print (cur_page)
            payload = {'ownerMemberId': ownerMemberId,
                       'productId': productId,
                       'page': cur_page,
                       'withPictures': 'true'}
            page = requests.post('https://feedback.aliexpress.com/display/productEvaluation.htm#feedback-list',
                                 data=payload)
            soup = BeautifulSoup(page.text, 'html.parser')

            feedback_items = soup.find_all('dl', class_='buyer-review')
            if len(feedback_items) < 1: break
            for fi in feedback_items:
                print('------------------')
                fi_date = fi.find('dd', class_='r-time')
                fi_date_format = re.sub(r"\s+", u"_", fi_date.get_text()).replace(':', '-')
                print(fi_date_format)
                fi_images = fi.find_all('img')

                if not os.path.exists('pics\\' + productId):
                    os.mkdir('pics\\' + productId)
                cnt = 1
                for img in fi_images:
                    print(img.get('src'))
                    file = requests.get(img.get('src'))
                    print('file=',file)
                    with open('.\\pics\\' + productId + '\\' + str(productId) + '_' + fi_date_format + '_' + str(cnt) + '.jpg', 'wb') as f:
                        f.write(file.content)
                    cnt = cnt + 1
                    import time
                    time.sleep(1)
            cur_page = cur_page + 1