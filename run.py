import os

import flask
from flask import Flask, request, make_response
import hashlib
import xmltodict
import time

from wx_reply import *
# wx_reply = Wx_Reply()

from sql_mode import *

app = Flask(__name__)


@app.route('/', methods=["GET"])
def wechat():
    # 设置token
    token = 'Fxhaoo'
    # 获取参数
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    # 先校验是否齐全
    if not all([signature, timestamp, nonce]):
        flask.abort(400)

    # 对参数进行字典排序，拼接字符串
    temp = [timestamp, nonce, token]
    temp.sort()
    temp = ''.join(temp)
    # 加密
    if hashlib.sha1(temp.encode("UTF-8")).hexdigest() == signature:
        return make_response(echostr)
    else:
        return make_response("认证失败")


@app.route('/', methods=["POST"])
def receive_msg():
    xml_str = request.data
    if not xml_str:
        flask.abort(400)
    # 解析消息
    xml_dict = xmltodict.parse(xml_str).get("xml")
    # 提取消息
    msg_type = xml_dict.get("MsgType")
    content = xml_dict.get("Content")
    tuser = xml_dict.get("ToUserName")
    fuser = xml_dict.get("FromUserName")
    openid = request.args.get('openid')
    if msg_type == "text":
        res = reg_msg(content, openid)
        return send_textContent(tuser, fuser, res)


def send_textContent(tuser, fuser, content):
    resp_dict = {
        "xml": {
            "ToUserName": tuser,
            "FromUserName": fuser,
            "CreateTime": int(time.time()),
            "MsgType": "text",
            "Content": content
        }
    }
    resp_xml_str = xmltodict.unparse(resp_dict)
    return resp_xml_str




if __name__ == '__main__':
    # init_db()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 80)))
