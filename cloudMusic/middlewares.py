# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

CHROMEDRIVER_PATH = "D:\python\chromedriver.exe"


class ChromeDriverMiddleware(object):

    def process_request(self, request, spider):
        if spider.name == "CloudMusic":
            print("Chrome(headless) is starting......")
            # chrome 无头版设置
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--ignore-certificate-errors')
            driver = webdriver.Chrome(
                executable_path=CHROMEDRIVER_PATH, chrome_options=options)
            # 启动chrome
            print("请求的url：", request.url)
            driver.get(request.url)
            # with open('bug.html', 'w', encoding='utf-8') as f:
            #     f.write(driver.page_source)
            driver.switch_to.frame('g_iframe')
            wait = ui.WebDriverWait(driver, 30)
            try:
                wait.until(lambda driver: driver.find_element(By.ID, 'm-pl-container'
                                                              ))
            except Exception:
                print('没有"m-pl-container"的标签，歌单推荐页')
            try:
                wait.until(
                    lambda driver: driver.find_element(By.CLASS_NAME, 'm-table'))
            except Exception:
                print('没有"m-table"的标签，歌单详情页')
            body = driver.page_source
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return


class CloudmusicSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CloudmusicDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
