import scrapy
import re
from weather.items import WeatherItem

class WeatherSpider(scrapy.Spider):
    name = "weather_spider"
    header  = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3226.400 QQBrowser/9.6.11681.400'
    }

    def start_requests(self):
        start_urls = ["/textFC/beijing.shtml",\
        "/textFC/anhui.shtml",\
        "/textFC/anhui.shtml",\
        "/textFC/chongqing.shtml",\
        "/textFC/gansu.shtml",\
        "/textFC/fujian.shtml",\
        "/textFC/guangdong.shtml",\
        "/textFC/guizhou.shtml",\
        "/textFC/guangxi.shtml",\
        "/textFC/hainan.shtml",\
        "/textFC/hebei.shtml",\
        "/textFC/henan.shtml",\
        "/textFC/hubei.shtml",\
        "/textFC/hunan.shtml",\
        "/textFC/heilongjiang.shtml",\
        "/textFC/jilin.shtml",\
        "/textFC/jiangsu.shtml",\
        "/textFC/jiangxi.shtml",\
        "/textFC/liaoning.shtml",\
        "/textFC/neimenggu.shtml",\
        "/textFC/ningxia.shtml",\
        "/textFC/qinghai.shtml",\
        "/textFC/shandong.shtml",\
        "/textFC/shan-xi.shtml",\
        "/textFC/shanxi.shtml",\
        "/textFC/shanghai.shtml",\
        "/textFC/sichuan.shtml",\
        "/textFC/tianjin.shtml",\
        "/textFC/xizang.shtml",\
        "/textFC/xinjiang.shtml",\
        "/textFC/yunnan.shtml",\
        "/textFC/zhejiang.shtml",\
        "/textFC/hongkong.shtml",\
        "/textFC/macao.shtml",\
        "/textFC/taiwan.shtml"]
        
        for url in start_urls:
            yield scrapy.Request("http://www.weather.com.cn" + url)


    def parse(self, response):

        global FLAG

        # print(response.body)
        item = WeatherItem()

        # citys = response.xpath('//div[@class="conMidtab" and not(@style)]/div[@class="conMidtab3"]/table/tbody/tr')
        citys = response.xpath('//div[@class="conMidtab" and not (@style)]/div[@class="conMidtab3"]/table/tr')

        for city in citys:
            item['city'] = city.xpath('./td[@width=83]/a/text()').get()
            item['weather_morning'] = city.xpath('./td[@width=89]/text()').get()
            item['weather_evening'] = city.xpath('./td[@width=98]/text()').get()

            # handle wind info
            wind_morning_list = city.xpath('./td[@width=162]').getall()
            for wind_morning in wind_morning_list:
                wind_morning_single = "".join(wind_morning.split())

                # remove HTML tag
                wind_morning_single_matched = re.sub(r'<.*?>', '', wind_morning_single)
                print(wind_morning_single_matched)
                wind_morning_single_matched2 = re.sub(r'&lt;', '<', wind_morning_single_matched)
                print(wind_morning_single_matched2)

                item['wind_morning'] = wind_morning_single_matched2

            wind_evening_list = city.xpath('./td[@width=177]').getall()
            for wind_evening in wind_evening_list:
                wind_evening_single = "".join(wind_evening.split())

                # remove HTML tag
                wind_evening_single_matched = re.sub(r'<.*?>', '', wind_evening_single)
                wind_evening_single_matched2 = re.sub(r'&lt;', '<', wind_evening_single_matched)

                item['wind_evening'] = wind_evening_single_matched2

            # get temperature from response
            item['temperature_high'] = city.xpath('./td[@width=92]/text()').get()
            item['temperature_low'] = city.xpath('./td[@width=86]/text()').get()

            yield item
