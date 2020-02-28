from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import abc
import six
from time import sleep
import time
import pandas as pd

remote_link="http://selenium:4444/wd/hub"
link_app="https://play.google.com/store/apps/details?id="

_ALL_REVIEWS={'en':'User reviews','pt':'Resenha completa'}
_MONTHS={'janeiro':'01',
         'fevereiro':'02',
         'marco':'03',
         'abril':'04',
         'maio':'05',
         'junho':'06',
         'julho':'07',
         'agosto':'08',
         'setembro':'09',
         'outubro':'10',
         'novembro':'11',
         'dezembro':'12'}
_SCROLL_PAUSE_TIME=3

#retorna se existe avaliação
def review_already_exists(review,all_reviews):
    for review_group in all_reviews:
        if review_group['review']==review:
            return True
        return False

#pega informações da avaliação
def get_information_review(review_element_child):
    review_text = review_element_child.find_element_by_xpath('./div[2]/div[2]/span[1]').text.strip()
    iduser = review_element_child.find_element_by_xpath('./div[1]/img').get_attribute("src").strip()
    name = review_element_child.find_element_by_xpath('./div[2]/div[1]/div[1]/span').text.strip()
    rating = review_element_child.find_element_by_xpath('./div[2]/div[1]/div[1]/div[1]/span[1]/div[1]/div[1]')\
        .get_attribute('aria-label').strip()
    date = review_element_child.find_element_by_xpath('./div[2]/div[1]/div[1]/div[1]/span[2]').text.strip()
    like = review_element_child.find_element_by_xpath('./div[2]/div[1]/div[2]/div/div[1]/div[2]').text.strip()
    name_answer = review_element_child.find_element_by_xpath('./div[2]/div[3]/div[2]/span[1]').text.strip()
    date_answer = review_element_child.find_element_by_xpath('./div[2]/div[3]/div[2]/span[2]').text.strip()
    answer = review_element_child.find_element_by_xpath('./div[2]/div[3]').text.strip()
    return dict(iduser=iduser,name=name,date=date,rating=rating,review_text=review_text,like=like,
                name_answer=name_answer,date_answer=date_answer,answer=answer)

@six.add_metaclass(abc.ABCMeta)
class CrawlerApp():

    def __init__(self,app_id,language,output):
        self.app_id=app_id
        self.language=language
        self.output=output
        self.remote_link=remote_link

    def init_driver(self):
        chrome_options=webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver=webdriver.Remote(self.remote_link,DesiredCapabilities.CHROME,options=chrome_options)
        print('Passei por: init_driver')
        return driver

    def run_reviews(self):
        for option in self._get_list_options():
            items1=self._get_item_listbox(0)
            items2=self._get_item_listbox(1)
            items_option1=items1[option[0]].text
            items_option2=items2[option[1]].text
            print(f'{items_option1},{items_option2}')
            items1[option[0]].click()
            sleep(_SCROLL_PAUSE_TIME)
            items2[option[1]].click()
            sleep(_SCROLL_PAUSE_TIME)
            self._scroll_page()
            self.collect_reviews().to_csv()
            #self.collect_reviews().to_csv(f"{self.output}/crawlerapp_{items_option1}_{items_option2}.csv")

    def getlink(self):
        link=f"{link_app}{self.app_id}&hl={self.language}&showAllReviews=true"
        driver=self.init_driver()
        driver.delete_all_cookies()
        driver.get(link)
        print('Passei por: getlink')
        return driver

    def select_all_reviews(self):
        x_path_review=f"//h3[contains(text(),'{_ALL_REVIEWS[self.language]}')]/following-sibling::div[1]"
        print('passei por: select_all_reviews')
        return self.getlink().find_element_by_xpath(x_path_review).find_elements_by_xpath('./*')

    def collect_reviews(self):
        all_reviews=[]
        for review in self.select_all_reviews():
            review_element_child=review.find_element_by_xpath('./div[1]')
            if review_element_child:
                review=get_information_review(review_element_child)
                all_reviews.append(review)
        data = pd.DataFrame(all_reviews)
        print('passei por collect reviews')
        return data

    def _get_item_listbox(self,index):
        listbox=self._get_listbox()
        listbox[index].click()
        sleep(_SCROLL_PAUSE_TIME)
        return listbox[index].find_elements_by_xpath("./div[2]/div[contains(@role, 'option')]")

    def _get_listbox(self):
        return self.getlink().find_elements_by_xpath("//div[contains(@role, 'listbox')]")

    def _scroll_page(self):
        driver=self.getlink()
        get_val_scroll="return document.documentElement.scrollHeight"
        val_scroll="window.scrollTo(0,document.documentElement.scrollHeight);"
        last_height=driver.execute_script(get_val_scroll)
        while True:
            driver.execute_script(val_scroll)
            time.sleep(_SCROLL_PAUSE_TIME)
            new_height=driver.execute_script(get_val_scroll)
            if new_height==last_height:
                break
            last_height=new_height

    def _get_list_options(self):
        items1=self._get_item_listbox(0)
        items2=self._get_item_listbox(1)
        return [[items1.index(x),items2.index(y)] for x in items1 for y in items2]


# fazer esse arquivo salvar essa informação em algum banco
# quebrar essa código para virar vários operadores