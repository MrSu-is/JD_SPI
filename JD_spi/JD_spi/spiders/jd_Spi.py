import scrapy
from selenium import webdriver
from scrapy_redis.spiders import RedisSpider
from ..items import JdSpiItem
from time import sleep
import redis
from urllib import parse


class JdSpiSpider(RedisSpider):
    name = 'jd_Spi'
    allowed_domains = ['jd.com']
    #start_urls = ['https://item.jd.com/100021980838.html']
    
    #pool = redis.ConnectionPool(host='192.168.31.246', port=6379, db=0)  
    #r = redis.Redis(connection_pool=pool)
    #urls = r.get('jd_Spi:start_urls')

    redis_key = "jd_Spi:start_urls"

    
    next_page = 1
     
    
    def __init__(self):
        super(JdSpiSpider,self).__init__()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(executable_path='F:\\阅读计划报告\chromedriver_win32 (1)\chromedriver.exe',chrome_options=options)

    def close(self,spider):
        self.driver.quit()
        print('Close The Spider')

    def parse(self, response):
        
        urls = response.url
        print(response.url)
        


        for i in range(2):
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            sleep(2)

        sleep(2)

        price = response.xpath('//*[@class = "p-price"]/strong/i/text()').extract()
        #picture = response.xpath('//*[@class = "p-img"]/a/img/@src').extract()
        title = response.xpath('//*[@class = "p-name p-name-type-2"]/a/em/text()').extract()
        shop = response.xpath('//*[@class = "curr-shop hd-shopname"]/text()').extract()
        end = response.xpath('//span[@class = "p-skip"]/em/b/text()').extract_first()
        #print(price)
        #print(list)
        #print(title)
        #brand = response.xpat('//*')
        i = 1
        print(end)
        goodsDtails = response.xpath('//*[@class = "p-name p-name-type-2"]/a/@href').extract()
        print(goodsDtails)
        for index,goodsDtail in enumerate(goodsDtails):
            title_detail = title[index]
            price_detail = price[index]
            #picture_detail = picture[index]
            shop_detail = shop[index]
            yield scrapy.Request(url = 'https:' + goodsDtail,callback=self.parseDetail,meta={'title_detail':title_detail,'price_detail':price_detail,'shop_detail':shop_detail},dont_filter=True)
        
        
        #a = self.driver.find_element_by_link_text('下一页')
        #a = self.driver.find_element_by_css_selector('a.pn-next')
        #a = self.driver.execute_script('document.getElementsByClassName("pn-next")[0].click()')
        #next_url = self.redis_key + str(self.page)
        #a = self.driver.find_elements_by_class_name("pn-next")[0]
        #li = [next_url]
        #print(next_url)
        #if self.page != end:
            # 发送下一个url地址请求，并指定处理响应的回调函数。
            #yield scrapy.Request(url=str(next_url), callback=self.parse,dont_filter=True)
        #if a:
            #a.click()
        

        #if(i<=int(end[0])):
        #    i += 1
        #    yield scrapy.Request(url = self.urls + '&page=' + str(2*i-1) + '&s=' + str(1+60*i),callback=self.parse,)
        base_url = urls
        print(base_url)
        headers = {'referer': response.url}
        self.next_page = self.next_page + 1
        if self.next_page<(2*int(end)):
            yield scrapy.Request(url = base_url + '&page=' + str(self.next_page),callback=self.parse,headers=headers)
    
    def parseDetail(self,response):
        brand = response.xpath('//*[@class = "p-parameter"]/li/a/text()').extract_first()
        goods_id = response.xpath('html/body/div[12]/div[1]/div[0]/div[0]/ul[1]/li[2]/text()').extract_first()
        #goods_id = response.xpath('//*[@class = "parameter2 p-parameter-list"]/text()').extract_first()
        title_detail = response.meta['title_detail']
        price_detail = response.meta['price_detail']
        #picture_detail = response.meta['picture_detail']
        shop_detail = response.meta['shop_detail']
        item = JdSpiItem()
        item['title_detail'] = title_detail
        item['price_detail'] = price_detail
        #item['picture_detaill'] = picture_detail
        item['shop_detail'] = shop_detail
        item['brand'] = brand
        item['goods_id'] = goods_id
        yield item
        #print(item)
        #print(abstract_detail,score)
        #describe = response.xpath('//*[@property = "v:summary"]/text()').extract_first()
        #pattern = '[a-zA-Z]+'
        #num = re.findall(pattern=pattern,string=describe)
        #print(num)
        pass