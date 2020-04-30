import requests
from bs4 import BeautifulSoup

page_start = 1
page_end = 2
search_mode = True
SRCH_PAGES = 10000
srch_page_start = 1
srch_page_end = 2

BASE_URL = "https://gall.dcinside.com/mgallery/board/lists/"
headers = {'User-Agent': 'Mozilla/5.0'}
params = {
    'id': 'tullius',
    'page': '1',
    's_type': '',
    's_keyword': '',
    'search_pos': ''
}


def searchByPage(page_start, page_end):
    for page in range(page_start, page_end + 1):
    
        params['page'] = str(page)

        req = requests.get(BASE_URL, params=params, headers=headers)

        # 밑에 print req를 했을때 response[200]이 나온다면 정상적으로 접속이 되었다는 뜻.
        # 만약 정상적인 접속이 이루어지지 않는다면 USER-Agent를 최신화해야 한다.
        #print(req)

        soup = BeautifulSoup(req.content, 'html.parser')

        table_contents = soup.find('tbody').find_all('tr')

        for item in table_contents:

            if item.find('b'): #공지나 광고일때 스킵
                continue

            gall_writer, gall_link, gall_subj, gall_num, gall_recommend = '작성자: ', '링크: ', '말머리: ', '번호: ', '추천수: '
            gall_title, gall_date, gall_view = '제목: ', '게시 일자: ', '조회수: '

            gall_link_tag = item.find('a')
            gall_title = gall_title + gall_link_tag.text
            raw_link = gall_link_tag.attrs['href']
            gall_link = gall_link + raw_link if 'http' in raw_link else ('https://gall.dcinside.com' + raw_link)

            gall_writer_tag = item.find('span', class_ = 'nickname')
            if gall_writer_tag:
                gall_writer = gall_writer + gall_writer_tag.text

            gall_writer_tag = item.find('span', class_ = 'ip')
            if gall_writer_tag:
                gall_writer = gall_writer + gall_writer_tag.text

            gall_subj = gall_subj + item.find('td', class_ = 'gall_subject').text
            gall_num = gall_num + item.find('td', class_ = 'gall_num').text
            gall_recommend = gall_recommend + item.find('td', class_ = 'gall_recommend').text

            gall_date_tag = item.find('td', class_ = 'gall_date')
            if 'title' in gall_date_tag.attrs:
                gall_date = gall_date + gall_date_tag.attrs['title']
            else:
                gall_date = gall_date + gall_date_tag.text

            gall_view = gall_view + item.find('td', class_ = 'gall_count').text

            print('--------------', gall_title, gall_link, gall_date, gall_writer, gall_num, gall_recommend, gall_view, gall_subj, sep = '\n')

if search_mode:
    #search_pos를 알기 위해서, 첫 페이지 첫 게시물의 갤러리 번호를 구한다.
    req = requests.get(BASE_URL, params=params, headers=headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    table_contents = soup.find('tbody').find_all('tr', class_ = 'ub-content us-post')
    
    for t_content in table_contents:
        
        cur_galtype = t_content.attrs['data-type']
        
        if cur_galtype == 'icon_txt' or cur_galtype == 'icon_pic':
            
            cur_gallnum = int(t_content.attrs['data-no'])
            break

    params['s_type'] = 'search_all'
    params['s_keyword'] = 'psq'
    
    #구한후 서치
    for c_srch_page in range(srch_page_start - 1, srch_page_end):
        
        params['page'] = '1'
        params['search_pos'] = str(-cur_gallnum + c_srch_page * SRCH_PAGES)
        req = requests.get(BASE_URL, params=params, headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        page_list = soup.find('div', class_ = 'bottom_paging_box')
        pages = page_list.find_all('a')
        pages_cnt = len(pages)
        if pages_cnt > 15:
            pgend_str = pages[-2].attrs['href']
            pages_cnt = int(pgend_str.split('page=')[1].split('&')[0])
        searchByPage(1, pages_cnt)
    
else:
    searchByPage(page_start, page_end)

'''
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.parse import quote_plus
 
baseUrl = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='
plusUrl = input('검색어 입력: ') 
crawl_num = int(input('크롤링할 갯수 입력(최대 50개): '))
 
url = baseUrl + quote_plus(plusUrl) # 한글 검색 자동 변환
html = urlopen(url)
soup = bs(html, "html.parser")
img = soup.find_all(class_='_img')
 
n = 1
for i in img:
    print(n)
    imgUrl = i['data-source']
    with urlopen(imgUrl) as f:
        with open('./images/img' + str(n)+'.jpg','wb') as h: # w - write b - binary
            img = f.read()
            h.write(img)
    n += 1
    if n > crawl_num:
        break
    
    
print('Image Crawling is done.')

'''