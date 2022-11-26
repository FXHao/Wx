import logging
import os

import flask
from flask import Flask, request, make_response
import hashlib
import xmltodict
import time
import json

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def wechat():
    if request.method == 'GET':
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
    if request.method == 'POST':
        user_message()


def user_message():
    xml_str = request.data
    if not xml_str:
        flask.abort(400)

    # 解析消息
    xml_dict = xmltodict.parse(xml_str).get("xml")

    # 提取消息
    msg_type = xml_dict.get("MsgType")
    if msg_type == "text":
        resp_dict = {
            "xml": {
                "ToUserName": xml_dict.get("FromUserName"),
                "FromUserName": xml_dict.get("ToUserName"),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": xml_dict.get("Content")
            }
        }
        resp_xml_str = xmltodict.unparse(resp_dict)

        return make_response(resp_xml_str)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 80)))
