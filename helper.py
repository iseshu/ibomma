import httpx
import json
from bs4 import BeautifulSoup
def get_mainpage():
  url = "https://ww5.ibomma.cx/telugu-movies/"
  req = httpx.get(url).text
  soup = BeautifulSoup(req,'html.parser')
  articles = soup.find_all('article',class_='post hentry')
  data = []
  for article in articles:
    dat = {
        "link":article.find('a')['href'],
        "title":article.find('h2',class_='entry-title').find('a').text,
        "image":article.find('img')['src'],
        "year":article.find('h2',class_='entry-title').find('span').text
    }
    data.append(dat)
  dta = {"status":True,"data":data}
  return dta


def search_movie(query):
  url = "https://idjhcxds-secure-v2.search-api.cloud/?label=telugu&q={}"
  imgurl = "https://i0.wp.com/{}?w=-230&quality=100"
  req = httpx.get(url.format(query),headers = {"Referer" : "https://seucre-otp-ymflg-h002giy-ig-india.ibc.wf/"}).text
  soup = BeautifulSoup(req,'html.parser')
  dat = ''
  for script in soup.find_all("script"): 
    if "data=" in script.text:
      dat = script.text.replace('data={},data= ','')
      break
  data = json.loads(dat)
  movie_data = []
  a= 0
  for i in data['hits']['hits']:
    if a ==2:
      a+=1
      continue
    data = i['_source']
    #print(data)
    movie_data.append({ 
        "title": data['title'].replace(' Watch Online & FREE DOWNLOAD - iBOMMA',''),
        "language": data['weblanguage'],
        "description": data['description'],
        "link":data['location'],
        "image": imgurl.format(data['image_link'].replace('https://',''))
    })
    a+=1
  return {"status":True,"data":movie_data}


def get_page(url):
  req = httpx.get(url).content
  soup = BeautifulSoup(req,'html.parser')
  if not soup.find('tbody'):
    try: 
      trailer = soup.find('a',class_='button-trailer-css vp-a external wplightbox')['href'] 
    except:
      trailer = None
    download_lin = soup.find('a',class_="button-download-css")['href']
    dwn_link = get_dwnlink(download_lin)
    data = {
        "link":url,
        "type":"movie",
        "title" : soup.find('div',class_="entry-title-movie").text,
        "trailer" : trailer,
        "description" : soup.find('div',class_="additional-info").text.replace('\nSynopsis: ',''),
        "dwn_link" : dwn_link
    }
  else:
    try: 
      trailer = soup.find('a',class_='button-trailer-css vp-a external wplightbox')['href'] 
    except:
      trailer = None
    episode_info = []
    a = 0
    for data in soup.find('tbody').find_all('tr'):
      a+=1
      #print(data)
      title = data.find('td',class_="ep-name").text
      dwn_lin = data.find('a',class_='button-dl-css')['href']
      dat = {"title":title,"episode no":a,"dwn_link":dwn_lin}
      episode_info.append(dat)
    data = {
        "link":url,
        "type":"series",
        "title" : soup.find('div',class_="entry-title-movie").text,
        "trailer" : trailer,
        "description" : soup.find('div',class_="additional-info").text.replace('\nSynopsis: ',''),
        "episode_info" : episode_info
        }
  return {"status":True,"data":data}
  
def get_dwnlink(link):
	req = httpx.get(link,headers = {"Referer" : "https://seucre-otp-ymflg-h002giy-ig-india.ibc.wf/"}).text
	soup1 = BeautifulSoup(req,'html.parser')
	return soup1.prettify()
