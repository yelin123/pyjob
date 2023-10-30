import yaml
import requests
import json
import logging
import time
import urllib3
import os
parent_dir = os.path.dirname(os.path.abspath(__file__))

from MyUtil import MyUtil
from Strategy import Strategy
urllib3.disable_warnings()
import schedule

def load_yaml(config_file):
    abs_path = parent_dir + '/' + config_file;
    print('config file path:' + abs_path)
    try:
        with open(abs_path, 'r') as f:
            config=yaml.safe_load(f)
            print("load config :" + str(config))
            return config
    except Exception as e:
        print(str(e))
    return None

try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

class FeiShuBot(object):
    def __init__(self):
        '''
        机器人初始化
        :param webhook: 飞书群自定义机器人webhook地址
        :param secret: 机器人安全设置页面勾选“加签”时需要传入的密钥
        :param pc_slide: 消息链接打开方式，默认False为浏览器打开，设置为True时为PC端侧边栏打开
        :param fail_notice: 消息发送失败提醒，默认为False不提醒，开发者可以根据返回的消息发送结果自行判断和处理
        '''
        super(FeiShuBot, self).__init__()
        self._headers = {'Content-Type': 'application/json; charset=utf-8'}

    def _post(self, data):
        self._web_hook = "https://open.feishu.cn/open-apis/bot/v2/hook/ee058c51-2dd8-4d15-b804-29a5ae6091c9"
        if self._web_hook is None:
            print('no valid web_hook or chat_group is selected')
            return
        try:
            post_data = json.dumps(data)
            response = requests.post(self._web_hook, headers=self._headers, data=post_data, verify=False)
            #print(response)
        except requests.exceptions.HTTPError as exc:
            logging.error("消息发送失败， HTTP error: %d, reason: %s" % (exc.response.status_code, exc.response.reason))
            raise
        except requests.exceptions.ConnectionError:
            logging.error("消息发送失败，HTTP connection error!")
            raise
        except requests.exceptions.Timeout:
            logging.error("消息发送失败，Timeout error!")
            raise
        except requests.exceptions.RequestException:
            logging.error("消息发送失败, Request Exception!")
            raise
        else:
            try:
                result = response.json()
            except JSONDecodeError:
                logging.error("服务器响应异常，状态码：%s，响应内容：%s" % (response.status_code, response.text))
                return {'errcode': 500, 'errmsg': '服务器响应异常'}
            else:
                logging.debug('发送结果：%s' % result)
                # 消息发送失败提醒（errcode 不为 0，表示消息发送异常），默认不提醒，开发者可以根据返回的消息发送结果自行判断和处理
                # if self._fail_notice and result.get('errcode', True):
                #     time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                #     error_data = {
                #         "msgtype": "text",
                #         "text": {
                #             "content": "[注意-自动通知]飞书机器人消息发送失败，时间：%s，原因：%s，请及时跟进，谢谢!" % (
                #                 time_now, result['errmsg'] if result.get('errmsg', False) else '未知异常')
                #         },
                #         "at": {
                #             "isAtAll": False
                #         }
                #     }
                #     logging.error("消息发送失败，自动通知：%s" % error_data)
                #     requests.post(self._web_hook, headers=self._headers, data=json.dumps(error_data))
                return result

    # -----------------public function-----------------
    def send_notification(self,title,message):
        # 打印按指定格式排版的时间
        current_time = MyUtil.now().strftime('%Y-%m-%d %H:%M:%S')
        print(current_time)
        report_content=[
            [   {"tag": "text", "text": "当前时间: {}".format(current_time)} ],
            [   {"tag": "text", "text": "{}".format(message)} ],
        ]
        print('send to feishu:')

        self._post({
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": report_content,
                    }
                }
            }
        })

fsb = FeiShuBot()
def job():
    fsb.send_notification("⏰ 正在执行自动化任务 ⏰","程序正在运行，持续为您服务")
    current_time = MyUtil.now().strftime('%Y-%m-%d %H:%M:%S')
    print(current_time +"  I'm working...")
    # 执行策略， 生成消息
    if not(MyUtil.isTradeDay(MyUtil.now())):
        fsb.send_notification("温馨提示","非交易时段，好好享受生活吧 ~ ")
        return
    
    stg = Strategy()
    res = stg.创业板1进2()
    if not(res is None):
        fsb.send_notification("创业板1进2",res)

    res2 = stg.主板1进2()
    if not(res2 is None):
        fsb.send_notification('主板1进2', res2)

    
if __name__ == "__main__":

    # schedule.every(5).seconds.do(job)
    # schedule.every(10).seconds.do(job)
    # schedule.every(0.25).minutes.do(job)
    # schedule.every().hour.do(job)
    config = load_yaml('config.yaml')
    print("程序开始运行")
    schedule.every().day.at('09:25:10').do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
