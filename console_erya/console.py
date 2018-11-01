# coding:utf-8
import time
from PIL import Image
from selenium import webdriver, common
# import matplotlib.pyplot as plt
from .config import *
from console_erya.log import *
from console_erya.questions import query_http_server
import os
from .automaticcompletion import AutomaticCompletion
from base64 import b64encode


class Console:
    status = {
        'search_school': 0,
        'select_school': 0,
        'login': 0,
        'get_course': 0,
        'browser_watch': 0
    }
    __base64_png = 'data:image/png;base64,'
    __select_school_result = []
    __course = []
    __course_lesson = []

    def __init__(self):
        # pass
        # prefs = {
        #     "profile.default_content_setting_values.plugins": 1,
        #     "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        #     "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        #     "PluginsAllowedForUrls": "https://chaoxing.com"
        # }
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--log-level=3')
        self.options.add_argument('--slient')
        self.options.add_argument('--disable-logging')
        self.options.add_argument('--mute-audio')
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1920,1080')
        # options.add_experimental_option("prefs", prefs)
        # self.driver = webdriver.Chrome(chrome_drive_path, chrome_options=options)
        # self.driver = webdriver.Chrome(chrome_drive_path)
        # self.driver.implicitly_wait(timeout)
        # try:
        #     self.driver.set_window_size(1920, 1080)
        # except common.exceptions.WebDriverException:
        #     logger.error(log_template, '出错', '无法调整窗口大小', '忽略此步骤')
        # self.driver.get(entrance_url)
        # self.get_login_ver_code()

    def quit(self):
        self.driver.quit()

    def init(self):
        self.driver = webdriver.Chrome(chrome_drive_path, chrome_options=self.options)
        self.driver.implicitly_wait(timeout)
        # try:
        #     self.driver.set_window_size(1920, 1080)
        # except common.exceptions.WebDriverException:
        #     logger.error(log_template, '出错', '无法调整窗口大小', '忽略此步骤')
        while True:
            self.driver.get(entrance_url)
            # print(self.driver.title)
            if '用户登录' not in self.driver.title:
                continue
            else:
                break
        

    def login(self, student_num, password, code):
        try:
            self.driver.find_element(login_code['type'], login_code['string']).clear()
        except common.exceptions.NoSuchElementException:
            self.driver.switch_to.frame(self.driver.find_elements_by_name('iframe')[0])
            self.driver.find_element(login_code['type'], login_code['string']).clear()
        self.driver.find_element(login_code['type'], login_code['string']).send_keys(code)
        self.driver.find_element(login_username['type'], login_username['string']).clear()
        self.driver.find_element(login_username['type'], login_username['string']).send_keys(student_num)
        self.driver.find_element(login_password['type'], login_password['string']).clear()
        self.driver.find_element(login_password['type'], login_password['string']).send_keys(password)
        self.driver.find_element(login_button['type'], login_button['string']).click()
        self.driver.switch_to.default_content()
        try:
            name = self.driver.find_element(login_ver['type'], login_ver['string']).text
        except common.exceptions.NoSuchElementException:
            try:
                result_text = self.driver.find_element(login_result['type'], login_result['string']).text
            except common.exceptions.NoSuchElementException:
                return 'False', False
            return str(result_text), False
        self.status['login'] = 1
        return str(name), True

    def search_school(self, school):
        """
        院校选择
        :param school:
        :return:
        """
        # 是否已经点击过院校选择按钮进入院校选择界面
        if not self.status['search_school']:
            self.driver.find_element(select_school_button['type'], select_school_button['string']).click()  # 点击选择院校按钮
        else:
            self.driver.find_element('css', '#dialog2 > div > div.zw_result > p > a').click()
        self.driver.find_element(select_school_search['type'], select_school_search['string']).clear()  # 清除搜索框
        self.driver.find_element(select_school_search['type'], select_school_search['string']).send_keys(school)  # 向搜索框填入院校
        self.driver.find_element(select_school_search_button['type'], select_school_search_button['string']).click()  # 院校搜索
        self.__select_school_result = self.driver.find_elements(select_school_result['type'], select_school_result['string'])
        self.status['search_school'] = 1
        return [x.text for x in self.__select_school_result]

    def select_school(self, id_: int):
        try:
            self.__select_school_result[id_].click()
        except (TypeError, IndexError):
            return False
        self.status['select_school'] = 1
        return True

    def get_login_ver_code(self, refresh=False, display=False):
        """
        获取验证码图片，保存为code.png
        :param refresh: 是否刷新
        :return:
        """
        code_path = os.path.join(temp_path, 'code.png')
        screen_shot = os.path.join(temp_path, 'screenshot.png')
        if refresh:
            self.driver.find_element(refresh_code['type'], refresh_code['string']).click()
            # self.operate(refresh_code['type'], refresh_code['string'], 'click')
        self.driver.get_screenshot_as_file(screen_shot)  # 保存登陆界面截图
        a = self.driver.find_element_by_id('numVerCode')  # 定位验证码
        l = a.location['x'] + 1
        t = a.location['y'] + 1
        r = a.location['x'] + a.size['width']
        b = a.location['y'] + a.size['height']
        im = Image.open(screen_shot)
        im = im.crop((l, t, r, b))
        im.save(code_path)
        if display:
            os.system(code_path)
            # time.sleep(5)
            # plt.figure("验证码")
            # plt.imshow(im)
            # plt.show()
            # im.show()
            # try:
            #     os.remove(path_)
            # except FileNotFoundError:
            #     pass
            # return True
        return code_path
        # result = self.__base64_png+b64encode(open(os.path.join(path_vercode, filename), 'rb').read()).decode()
        # try:
        #     os.remove('code.png')
        #     os.remove(os.path.join(path_vercode, filename))
        # except OSError:
        #     pass
        # return result

    def get_course(self):
        self.__course = []
        self.driver.switch_to.default_content()
        try:
            self.driver.find_element(lesson_index['type'], lesson_index['string']).click()
        except common.exceptions.NoSuchElementException:
            pass
        except:
            pass
        for x in course_name_list_frame:
            # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        for x in self.driver.find_elements(course_name_list['type'], course_name_list['string']):
            if not x.text:
                continue
            self.__course.append(x)
            # try:
            #     if x.text.split(remove_irrelevant_course[0])[remove_irrelevant_course[1]].strip() == remove_irrelevant_course[2]:
            #         continue
            #     self.__course.append(x)
            # except IndexError:
            #     continue
        self.status['get_course'] = 1
        return [x.text for x in self.__course]

    def browse_watch(self, course_id):
        try:
            course_id = int(course_id)
        except (TypeError, ValueError):
            return False
        if (course_id > (len(self.__course) - 1)) or (course_id < 0):
            return False
        course = self.__course[course_id]
        course_name = course.text
        course.click()
        time.sleep(5)
        for x in self.driver.window_handles:
            self.driver.switch_to.window(x)
            if self.driver.title == course_page_title:
                break
        self.driver.find_elements(first_lesson['type'], first_lesson['string'])[0].click()
        # time.sleep(5)
        # 是否已完成
        # complete_status = self.driver.find_elements(list_complete_status['type'], list_complete_status['string'])
        # # 课时链接、课时名称、完成状态
        # for x, y, z in zip(self.driver.find_elements(course_lesson_link['type'], course_lesson_link['string']), self.driver.find_elements(course_lesson_name['type'], course_lesson_name['string']), complete_status):
        #     if z.get_attribute('class') == list_em_complete_class:
        #         continue
        #     tmp = {'name': y.text.replace('\n', '').strip(), 'link': x.get_attribute('href')}
        #     self.__course_lesson.append(tmp)
        # self.driver.close()
        AutomaticCompletion(driver=self.driver, course_name=course_name).start()
        self.status['browser_watch'] = 1
        return True

    # def operate(self, type_, string, op, args=None):
    #     """
    #     部分点击、输入等操作
    #     :param type_:
    #     :param string:
    #     :param op:
    #     :param args:
    #     :return:
    #     """
    #     if op == 'click':
    #         self.driver.find_element(by=type_, value=string).click()
    #     elif op == 'send_key':
    #         self.driver.find_element(by=type_, value=string).clear()
    #         self.driver.find_element(by=type_, value=string).send_keys(args)


class Exam:
    __select = ''.join([chr(x) for x in range(65, 91)])

    def __init__(self):
        self.driver = webdriver.Chrome(chrome_drive_path)
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(timeout)
        self.driver.get(entrance_url)

    def start(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        a = self.driver.find_element_by_class_name('leftCardChild')
        typ = [(x, y.text.strip()) for x, y in enumerate(a.find_elements_by_tag_name('h3'))]
        for index, value in typ:
            z = 0
            a = self.driver.find_element_by_class_name('leftCardChild')
            le = len(a.find_elements_by_tag_name('div')[index].find_elements_by_tag_name('a'))
            for x in range(0, le):
                z += 1
                a = self.driver.find_element_by_class_name('leftCardChild')
                a.find_elements_by_tag_name('div')[index].find_elements_by_tag_name('a')[x].click()
                time.sleep(3)
                title = self.driver.find_element_by_xpath(
                    '//*[@id="submitTest"]//div[@class="Cy_TItle clearfix"]/div').text.strip().rstrip('分）').rstrip(
                    '0123456789').rstrip('.').rstrip('0123456789').rstrip('（').strip()
                last_title = title
                right_answer = query_http_server(op='query', test_type=value, title=title)
                logger.info(log_template, '查询', title, 'answer:{0}'.format(str(right_answer)))
                if value == '判断题':
                    if right_answer:
                        self.driver.find_elements_by_xpath('//*[@id="submitTest"]//ul[@class="Cy_ulBottom clearfix"]//li')[0].click()
                    else:
                        self.driver.find_elements_by_xpath('//*[@id="submitTest"]//ul[@class="Cy_ulBottom clearfix"]//li')[1].click()
                elif value in ['单选题', '多选题']:
                    tag = 0
                    if right_answer:
                        for y in self.driver.find_elements_by_xpath('//*[@id="submitTest"]//ul[@class="Cy_ulTop w-top"]/li'):
                            if y.text.strip().lstrip(self.__select).lstrip('、').strip() in right_answer:
                                y.click()
                                tag = 1
                    if not tag:
                        logger.error(log_template, str(z)+':'+value, title, '未查到，选择第一项')
                        self.driver.find_elements_by_xpath('//*[@id="submitTest"]//ul[@class="Cy_ulTop w-top"]/li')[0].click()
                else:
                    logger.error(log_template, value, title, '不支持该题型')
                # time.sleep(15)

