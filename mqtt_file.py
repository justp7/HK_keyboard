#!/usr/bin/env python
# -*- coding:utf-8 -*-
import paho.mqtt.client as mqtt  #引入MQtt库


import tkinter_label
import TrayIcon



client = mqtt.Client(client_id="keyport")  # 申请MQTT服务
MQTTStatus = 0  # MQTT链接状态标志位

def on_connect(client, userdata, flags, rc):
    global MQTTStatus
    print("Connected with result code " + str(rc))
    if rc == 0:
        # 连接成功
        MQTTStatus = 1  # 连接成功
    else:
        MQTTStatus = 0  # 连接失败


def on_subscribe(client, userdata, mid, granted_qos):
    print("消息发送成功")


def Mqtt_Status(tip, hoststr, port, self):
    global client, MQTTStatus

    if tip.get() == "链接":
        client.username_pw_set("admin", "password")  # 设置密码
        client.on_connect = on_connect  # 链接成功的回调
        client.on_subscribe = on_subscribe  # 消息发送成功的回调
        try:  # 尝试链接
            client.connect(host=str(hoststr), port=int(port), keepalive=60)  # 连接到MQTT服务端
            client.loop_start()  # 启动MQTT线程
            MQTTStatus = 1
            tip.set("断开")
            tkinter_label.MQTTStatusUpdata(self)
        except Exception as e:
            tkinter_label.error_msg("mqtt error")  # MQTT异常弹窗
            pass
    elif tip.get() == "断开":
        client.disconnect()  # 断开MQTT
        client.loop_stop()  # 停止MQTT线程
        tip.set("链接")
        tkinter_label.MQTTStatusUpdata(self)


def Mqtt_send(msg):
    global MQTTStatus
    if MQTTStatus == 1:
        client.publish(topic="portmsg", payload=str(msg), qos=0)
    else:
        if TrayIcon.minimize:
            print("publish fail")
        else:
            tkinter_label.error_msg("publish fail")

# MQTT测试函数 测试成功
def Mqtt_test():
    client.publish(topic="portmsg", payload="hello world", qos=0)

