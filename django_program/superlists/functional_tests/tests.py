#-*- coding:utf-8 -*-
import threading

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
import sys

# class NewVisitorTest(LiveServerTestCase):
class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                # cls.live_server_url = cls.server_url
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()


    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='/Users/apple/Documents/workspace/drivers/Firefox_driver/geckodriver')
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
            
        #伊迪丝听说有一个很酷的在线待办事项应用
        #她去看了这个应用的首页
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.server_url)

        #她注意到网页的标题头都包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title) 
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        #应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        
        #她在一个文本框中输入了“Buy peacock feathers”
        #伊迪丝的爱好是使用假蝇作饵钓鱼
        inputbox.send_keys('Buy peacock feathers')

        #她按回车键后，被带到了一个新的URL
        #这个页面的待办事项清单中显示了“1:Buy peacock feathers”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)   #需要一点时间，才能让页面的URL完成加载，让current_url获取到期望的地址
        edith_list_url = self.browser.current_url

        self.assertRegex(edith_list_url,'/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')


        
        # table = self.browser.find_element_by_id('id_list_table')
        # #在table标签中找tr标签，若使用element则会在用户未添加任何信息时报错，而用elements，则在内容未空时依然能进行下去
        # rows = table.find_elements_by_tag_name('tr')
        # # self.assertTrue(any(row.text == '1:Buy peacock feathers' for row in rows),
        # #                 "New to-do item did not appear in table--its text was:\n%s" %(table.text,))
        # self.assertIn('1:Buy peacock feathers',[row.text for row in rows])

        #页面中又显示了一个文本框，可以输入其他的待办事项
        #她输入了“Use peacock feathers to make a fly”
        #伊迪丝做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)  #用来缓冲刷新时间，如果不加，下面的find系列语句可能会报刷新的错误StaleElementReferenceException
        
        #页面再次更新，她的清单中显示了这两个待办事项
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.check_for_row_in_list_table('1:Buy peacock feathers')
        # self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        
        #现在一个叫做弗朗西斯的新用户访问了网站

        ##我们使用一个新浏览器回话
        ##确保伊迪丝的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #弗朗西斯访问首页
        #页面中看不到伊迪丝的清单
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        #弗朗西斯输入一个新的待办事项，新建一个清单
        #他不像伊迪丝那样兴趣盎然
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #弗朗西斯获得了他的唯一URL
        francis_list_url = self.browser.current_url

        time.sleep(1)  #遗留一个问题，相同的URL的时候，这里只能获取到前半部分的URL，后面的获取不到
                       #原来还是缓冲时间的问题，缓冲时间要加在回车之后，获取URL语句之前
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        #这个页面还是没有伊迪丝的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk',page_text)

        #两人都很满意，去睡觉了

    def test_layout_and_styling(self):
        #伊迪丝访问首页
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024,768)

        #她看到输入框完美的居中显示
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2, 512, delta=5)

        #她新建了一个清单，看到输入框仍能完美的居中显示
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)#等到页面完成加载，才能不在断言的时候报错
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2,512,delta=5)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
    #warnings提示，在eclipse中运行时，该提示不影响，最后显示未finish the test。若在终端运行，则只提示该warnings提示，而不会提示测试结束，删掉warnings后，在终端运行就正常了
    #该问题有待解决,是因为ignore写成了ignore
    #但是另外一个问题，为什么在eclipse中运行，没有报相同的错误

