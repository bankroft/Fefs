# coding:utf-8
import time
import os
import re
import threading
from .config import folder_temp_path
from .config import AutomaticcompletionConfig as ac
from .questions import query_http_server
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium import common
from random import randint
import requests
from random import choices
from string import ascii_letters
from .printinfo import print_info, print_progress


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

# class AutomaticCompletion(threading.Thread):
class AutomaticCompletion:
    # 生成choices(string.printable, k=16)
    __select = ''.join([chr(x) for x in range(65, 91)])
    __course = []
    __js = 'window.open("{0}");'

    def __init__(self, driver, course_name=''):
        # threading.Thread.__init__(self)
        self.driver = driver
        self.course_name = course_name

    def run(self):
        last_lesson = None
        retry = 3
        refresh_tag = 0
        while True:
            try:
                self.driver.refresh()
                self.driver.switch_to.default_content()
                les = self.driver.find_element(ac.not_completed_lesson['type'], ac.not_completed_lesson['string'])
                ActionChains(self.driver).click(les).perform()
                time.sleep(5)
                now_lesson = self.driver.find_element(ac.lesson_name['type'], ac.lesson_name['string']).text
                if last_lesson == now_lesson:
                    if retry == 0:
                        print_info(['出错', '无法检测视频(【{0}】)状态,请关闭程序手动观看该节课程'.format(last_lesson), '重试'], 'verbose', True, all_output=True)
                        return False, False
                    else:
                        print_info(['出错', '视频(【{0}】)播放错误'.format(last_lesson), '重试'], 'warning', True, all_output=True)
                        retry -= 1
                    if refresh_tag:
                        refresh_tag = 0
                    else:
                        print_info(['刷新页面', '视频(【{0}】)'.format(last_lesson), '刷新'], 'warning', True, all_output=True)
                        self.driver.refresh()
                        refresh_tag = 1
                        retry += 1
                        continue
                else:
                    retry = 3
                last_lesson = self.driver.find_element(ac.lesson_name['type'], ac.lesson_name['string']).text
                print_info(['开始观看', now_lesson, '开始'], 'info', True)
                if self.__watch():
                    last_lesson = None
                    print_info(['视频', now_lesson, '完成'], 'info', True)
                else:
                    continue
                print_info(['章节测验', now_lesson, '开始'], 'info', True)
                ans = self.__answer()
                print_info(['章节测验', now_lesson, '完成'], 'info', True)
                print_info(['更新正确题目', now_lesson, '开始'], 'info', True)
                updb = self.__update_db()
                print_info(['更新正确题目', now_lesson, '完成'], 'info', True)
                self.driver.get_screenshot_as_file(os.path.join(folder_temp_path, ''.join(choices(ascii_letters, k=8))+'.png'))
                if not ans and not updb:
                    if now_lesson.strip() == '阅读':
                        print_info(['出错', '阅读页面', '请手动完成'], 'error', timz=True, all_output=True)
                        return False, False
                # time.sleep(10)
            except common.exceptions.NoSuchElementException:
                break
        print_info(['课程', self.course_name if self.course_name else '没记录课程名字', '完成'], 'info', True)
        return True

    def switch_to_video_frame(self):
        self.driver.switch_to.default_content()
        for x in ac.learn_page_video_iframe:
            # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])

    def play_status(self):
        # self.switch_to_video_frame()
        self.__screenshot_video(os.path.join(folder_temp_path, str(0) + '.png'))
        time.sleep(5)
        # 秒
        progress = -1
        self.__screenshot_video(os.path.join(folder_temp_path, str(1) + '.png'))
        if open(os.path.join(folder_temp_path, str(0) + '.png'), 'rb').read() != open(os.path.join(folder_temp_path, str(1) + '.png'), 'rb').read():
            self.switch_to_video_frame()
            try:
                a = int(float(self.driver.find_element(ac.video_object['type'], ac.video_object['string']).get_attribute('duration')))
                b = int(float(self.driver.find_element(ac.video_object['type'], ac.video_object['string']).get_attribute('currentTime')))
                progress = b, a
            except common.exceptions.NoSuchElementException:
                pass
            except (TypeError, ValueError):
                pass
        else:
            return False, 'not play'
        return True, progress

    def answer_video(self, qt=None):
        """

        :param qt:题目类型
        :return:
        """
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        mid = self.driver.find_element_by_tag_name('iframe').get_attribute('mid')
        dc = int(time.time()*1000)
        try:
            res = requests.get(url=ac.video_answer_url.format(mid, dc), headers=headers).json()
        except requests.exceptions.ConnectionError:
            print_info(['视频答题', '获取失败', '返回'], 'warning', True)
            return False
        print_info(['视频答题', res[0]['datas'][0]['description'], '正在处理'], 'info', True)
        self.switch_to_video_frame()
        for k, d in enumerate(res[0]['datas'][0]['options']):
            if d['isRight']:
                self.driver.find_element_by_xpath('//div[@class="ans-videoquiz-title"]/../ul/li[' + str(k+1) + ']/label').click()
        self.driver.find_element_by_xpath('//div[@class="ans-videoquiz-title"]/../div[2]').click()
        print_info(['视频答题', res[0]['datas'][0]['description'], '完成'], 'info', True)

    def click_video(self):
        self.switch_to_video_frame()
        self.driver.find_element_by_id('video').click()

    def video_complete_status(self):
        self.driver.switch_to.default_content()
        for x in ac.learn_page_video_part_iframe:
            # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        try:
            self.driver.find_element(ac.video_complete_status['type'], ac.video_complete_status['string'])
            return True
        except common.exceptions.NoSuchElementException:
            pass
        try:
            self.driver.find_element(ac.video_not_complete_status['type'], ac.video_not_complete_status['string'])
            return False
        except common.exceptions.NoSuchElementException:
            return True

    def __watch(self):
        self.driver.switch_to.default_content()
        # 视频学习部分
        try:
            self.driver.find_element(ac.learn_page_video_button['type'], ac.learn_page_video_button['string']).click()
            # time.sleep(2)
        except common.exceptions.NoSuchElementException:
            return True
        # ct: 改变线路，a: 回答,s: 点击开始
        last_opt = None
        self.switch_to_video_frame()
        self.click_video()
        print_info(['点击视频', '启动', '完成'], 'info', True)
        # self.driver.find_element_by_xpath('//*[@id="video"]/button').click()
        # time.sleep(1)
        while True:
            # 该视频是否完成
            if self.video_complete_status():
                break
            self.switch_to_video_frame()
            a = self.play_status()
            if a[0]:
                # print(1)
                if a[1] != -1:
                    b = str(a[1][0]) + '/' + str(a[1][1])+'s'
                    p = str(int((a[1][0] / a[1][1])*100))
                    print_progress('滴 - 当前进度:{0} - {1}%'.format(b, p))
                last_opt = None
            else:
                try:
                    # 视频因格式不支持或者服务器或网络的问题无法加载。
                    text = self.driver.find_element_by_xpath('//*[@aria-label="弹窗"]/div[2]/div').text.strip()
                    # 是否正确切换线路
                    tmp = False
                    if '视频因格式不支持或者服务器或网络的问题无法加载' in text:
                        for x in self.driver.find_elements_by_xpath('//*[@aria-label="弹窗"]/div[2]/ul/li/label'):
                            if x.text.strip() == ac.internet_line:
                                print_info(['切换线路', ac.internet_line, '完成'], 'info', True)
                                x.click()
                                tmp = True
                                time.sleep(3)
                        # if not self.internet_line():
                        #     return False
                        last_opt = 'ct'
                        if not tmp:
                            print_info(['切换线路', ac.internet_line, '失败'], 'notice', True)
                            # logger.error(log_template, '切换线路', internet_line, '失败')
                            return False
                        else:
                            continue
                    elif '由于视频文件损坏或是该视频使用了你的浏览器不支持的功能，播放终止' in text:
                        # logger.error(log_template, '错误', '未知错误', '重新开始？')
                        print_info(['错误', '未知错误', '重新开始'], 'warning', True)
                        return False
                except common.exceptions.NoSuchElementException:
                    pass
                except IndexError:
                    pass
                # print(123)
                try:
                    # text = self.driver.find_element_by_xpath('//div[@class="ans-videoquiz-title"]').text.strip()
                    # print(33)
                    self.driver.find_element_by_xpath('//div[@class="ans-videoquiz-title"]')
                    self.answer_video()
                    last_opt = 'a'
                    # if text[1:4] == '判断题':
                        # self.answer_video(text[1:4])
                    continue
                except common.exceptions.NoSuchElementException:
                    pass
                # print(2)
                if last_opt == 's':
                    return False
                print_info(['点击视频', '启动', '完成'], 'info', True)
                # logger.info(log_template, '点击视频', '启动', '成功')
                self.click_video()
                last_opt = 's'
        return True

    def __answer(self):
        sleep_time = 10
        self.driver.switch_to.default_content()
        # 章节测试答题部分
        try:
            self.driver.find_element(ac.learn_page_test_button['type'], ac.learn_page_test_button['string']).click()
        except common.exceptions.NoSuchElementException:
            return False
        except common.exceptions.StaleElementReferenceException:
            return False
        start_time = time.time()
        while True:
            if time.time() - start_time > 10:
                print_info(['回答', '检测答题', '超时'], 'warning', True)
                # logger.error(log_template, '回答', '检测答题', '超时')
                return False
            time.sleep(3)
            self.driver.switch_to.default_content()
            try:
                for x in ac.test_load_complete_tag_iframe:
                    # driver.switch_to.frame(driver.find_elements_by_tag_name(x['name'])[x['index']])
                    self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
            except IndexError:
                continue
            try:
                # 页面是否加载完成
                self.driver.find_element(ac.test_load_complete_tag['type'], ac.test_load_complete_tag['string'])
            except common.exceptions.NoSuchElementException:
                print_info(['Error', 'Unknown error', 'Continue'], 'warning', True)
                continue
            break
        self.driver.switch_to.default_content()
        for x in ac.learn_page_test_status_iframe:
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        try:
            # xpath可能有问题
            self.driver.find_element(ac.test_complete_stataus['type'], ac.test_complete_stataus['string'])
            return True
        except common.exceptions.NoSuchElementException:
            pass
        self.driver.switch_to.default_content()
        for x in ac.learn_page_test_iframe:
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        tmp = self.driver
        while True:
            try:
                tmp = tmp.find_element_by_class_name(ac.Timu['string'])
            except common.exceptions.NoSuchElementException:
                break
            title = tmp.find_element_by_class_name('clearfix').text.strip('1234567890').replace('\n', '').strip()
            test_type = title[1:4]
            if test_type not in ['判断题', '单选题', '多选题']:
                print_info(['查询', test_type + '暂不支持', '跳过'], 'notice', True)
                continue
            right_answer = query_http_server(op='query', test_type=test_type, title=title[5:])
            if test_type == '判断题':
                if right_answer[0]:
                    if right_answer[2]:
                        print_info(['查询到', title, '正确'], 'info', True)
                        tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('label')[0].click()
                    else:
                        print_info(['查询到', title, '错误'], 'info', True)
                        tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('label')[1].click()
                else:
                    print_info(['判断', title, '未查到，选择正确'], 'notice', True)
                    tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('label')[0].click()
            else:
                tag = 0
                if right_answer[0]:
                    print_info(['查询到', title, ' '.join(right_answer[2])], 'info', True)
                    for x in tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('li'):
                        if x.text.split('\n')[1].strip() in right_answer[2]:
                            tag = 1
                            x.click()
                if not tag:
                    if right_answer[3] in ['token', 'open']:
                        print_info(['答案错误', title, '重新查询'], 'info', True)
                        right_answer = query_http_server(op='query', defalut=False, test_type=test_type, title=title[5:])
                        tag = 0
                        if right_answer[0]:
                            print_info(['查询到', title, ' '.join(right_answer[2])], 'info', True)
                            for x in tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('li'):
                                if x.text.split('\n')[1].strip() in right_answer[2]:
                                    tag = 1
                                    x.click()
                        if tag:
                            continue
                    print_info(['查询失败', title, '随机选择一项'], 'notice', True)
                    # logger.warning(log_template, '查询答案失败', title, '随机选择一项')
                    sleep_time = 60*ac.noanswer_sleep
                    # 未搜索到该题目答案，随机选择一项
                    tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('li')[randint(0, len(tmp.find_elements_by_tag_name('ul')[0].find_elements_by_tag_name('li'))-1)].click()
        # 提交部分
        print_info(['提交章节测试', '如果有未查到的单/多选题会等待{0}分钟提交，默认10s后提交'.format(ac.noanswer_sleep.__str__()), '等待'], 'info', timz=True, all_output=True)
        time.sleep(sleep_time)
        self.driver.switch_to.default_content()
        for x in ac.test_submit_iframe:
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        self.driver.find_element(ac.submit_test['type'], ac.submit_test['string']).click()
        time.sleep(2)
        while True:
            if self.driver.find_element(ac.submit_test_confirm['type'], ac.submit_test_confirm['string']).text != '确定':
                tmp = self.driver.find_element(ac.submit_test_validate['type'], ac.submit_test_validate['string'])
                if tmp.is_displayed():
                    os.system(self.__screenshot_sbt_validate())
                    code = input('验证码:').strip()
                    self.driver.find_element(ac.submit_test_code_input['type'], ac.submit_test_code_input['string']).clear()
                    self.driver.find_element(ac.submit_test_code_input['type'], ac.submit_test_code_input['string']).send_keys(code)
                    self.driver.find_element(ac.submit_test_code_button['type'], ac.submit_test_code_button['string']).click()
            else:
                break
        self.driver.find_element(ac.submit_test_confirm['type'], ac.submit_test_confirm['string']).click()
        print_info(['提交章节测试', '确认', '提交'], 'info', True)

    def __update_db(self):
        start_time = time.time()
        while True:
            if time.time() - start_time > 10:
                print_info(['更新题库', '检测超时', '跳过'], 'warning', True)
                return False
            time.sleep(3)
            self.driver.switch_to.default_content()
            try:
                for x in ac.test_load_complete_tag_iframe:
                    self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
            except IndexError:
                continue
            try:
                # 页面是否加载完成
                self.driver.find_element(ac.test_load_complete_tag['type'], ac.test_load_complete_tag['string'])
            except common.exceptions.NoSuchElementException:
                print_info(['错误', '测验页面加载未知错误', '重试'], 'warning', True)
                continue
            break
        self.driver.switch_to.default_content()
        for x in ac.learn_page_test_iframe_updatedb:
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        for x in self.driver.find_elements_by_class_name('TiMu'):
            title = x.find_elements_by_tag_name('div')[1].text.strip().replace('\n', '')
            test_type = title[1:4]
            if test_type not in ['判断题', '单选题', '多选题']:
                print_info(['更新题库', test_type + '暂不支持', '跳过'], 'notice', True)
                continue
            try:
                # 选择题正确icon
                right_or_wrong = x.find_element_by_tag_name('form').find_element_by_tag_name('div').find_element_by_tag_name('i').get_attribute('class')
            except (common.exceptions.NoSuchElementException, IndexError):
                # 判断题正确icon
                right_or_wrong = x.find_elements_by_tag_name('div')[4].find_elements_by_tag_name('i')[1].get_attribute('class')
            if right_or_wrong == 'fr dui':
                my_answer = x.find_elements_by_tag_name('div')[4].text.split('\n')[0].strip('我的答案：').strip()
                if test_type == '判断题':
                    if query_http_server(op='update', title=title[5:], test_type=test_type, answer=my_answer.strip()):
                        print_info(['更新题库', title + '\t答案: ' + my_answer, '成功'], 'info', True)
                    else:
                        print_info(['更新题库', title + '\t答案: ' + my_answer, '失败'], 'warning', True)
                else:
                    ma = re.findall('[{0}]'.format(self.__select), my_answer)
                    r = []
                    for y in ma:
                        r.append(x.find_elements_by_tag_name('li')[self.__select.index(y)].text.strip(self.__select).strip('、').strip())
                    answer = '&'.join(r)
                    if query_http_server(op='update', title=title[5:], test_type=test_type, answer=answer.strip()):
                        print_info(['更新题库', title + '\t答案: ' + answer, '成功'], 'info', True)
                    else:
                        print_info(['更新题库', title + '\t答案: ' + answer, '失败'], 'warning', True)
            elif right_or_wrong == 'fr bandui':
                pass

    def __screenshot_video(self, filename):
        self.driver.get_screenshot_as_file('tmp.png')
        self.driver.switch_to.default_content()
        for x in ac.learn_page_video_iframe:
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name(x['name'])[x['index']])
        tmp = self.driver.find_element_by_id('video_html5_api')
        size = tmp.size
        view = tmp.location_once_scrolled_into_view
        i = Image.open('tmp.png')
        i.crop(
            (
                view['x'],
                view['y'],
                view['x'] + size['width'],
                view['y'] + size['height']
            )
        ).save(filename)
        try:
            os.remove('tmp.png')
        except (FileNotFoundError, PermissionError):
            pass

    def __screenshot_sbt_validate(self, filename=os.path.join(folder_temp_path, 'sbtcode.png')):
        self.driver.get_screenshot_as_file('tmp.png')
        self.driver.switch_to.default_content()
        tmp = self.driver.find_element(ac.submit_test_imgcode['type'], ac.submit_test_imgcode['string'])
        i = Image.open('tmp.png')
        i.crop(
            (
                tmp.location_once_scrolled_into_view['x'],
                tmp.location_once_scrolled_into_view['y'],
                tmp.location_once_scrolled_into_view['x'] + tmp.size['width'],
                tmp.location_once_scrolled_into_view['y'] + tmp.size['height']
            )
        ).save(filename)
        try:
            os.remove('tmp.png')
        except (FileNotFoundError, PermissionError):
            pass
        return filename
