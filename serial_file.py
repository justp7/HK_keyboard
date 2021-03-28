#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import time    # 时间模块
import serial  # 串口模块
import threading  # 多线程
import re      # 分割
import serial.tools.list_ports
from serial import SerialException

import main  # main.py的函数
import tkinter_label
import mqtt_file  # mqtt相关操作


ser = serial.Serial()
threading_flag = False
# 获取串口号
def GetCom(self):
    port_list = list(serial.tools.list_ports.comports())
    portcnt = len(port_list)
    serial_com = []
    for m in range(portcnt):
        port_list_1 = list(port_list[m])
        serial_com.append(port_list_1[1])
    tkinter_label.com_refresh(self, serial_com)  # 刷新串口列表
    return serial_com



# 串口打开关闭函数
def usart_open(com, tip, button_var):
    global ser, threading_flag
    # multiprocessing.freeze_support()
    port_list = list(serial.tools.list_ports.comports())
    if button_var.get() == "打开串口" and int(len(port_list)) > 0:
        button_var.set("关闭串口")
        com = re.findall(r"[(](.*?)[)]", com)[0]  # 取出（）内端口数据
        try:
            ser = serial.Serial(
                port=com,
                baudrate=9600,
                parity="N",
                timeout=0.2,
                stopbits=float(1),
                bytesize=int(8))
            status = 1  # 打开串口
        except SerialException:
            status = 0  # 打开失败
            tip.set("打开异常")
            button_var.set("打开串口")
        if ser.is_open:
            recv_data = threading.Thread(target=thread_recv)
            recv_data.start()
            threading_flag = True
            tip.set("打开成功")
            pass
    else:
        button_var.set("打开串口")
        if ser.is_open:
            ser.close()  # 关闭串口
            tip.set("请选择串口")
            threading_flag = False
            # recv.terminate()  # 终止进程
        else:
            ser.close()  # 关闭串口
            status = 0  # 串口关闭
            pass


def test(text):
    print(text)


# 关闭串口服务函数
def close_serial():
    try:
        ser.close()
    except SerialException:
        pass


# 串口接收线程
def thread_recv():
    while True:
        try:
            # print("run")
            read = ser.readline().decode('utf-8')
            # print(len(read))
            if len(read) > 0:
                str_get=read.split("\r")
                # print(str_get[0])
                presskey(str_get[0])
            time.sleep(0.001)
        except Exception as e:
            time.sleep(0.01)
            # print("error")
            pass

# 执行 键盘按压 或者是MQTT消息
def presskey(ID):
    print(ID)
    if ID == '1':  # 机械按键1
        if not tkinter_label.var[0]:  # MQTT服务未绑定
            main.PressKey(main.M1)
            print("recieve m1")
        else:
            mqtt_file.Mqtt_send("M1")
    elif ID == '2':  # 机械按键2
        if not tkinter_label.var[1]:  # MQTT服务未绑定
            main.PressKey(main.M2)
            print("recieve m2")
        else:
            mqtt_file.Mqtt_send("M2")
    elif ID == '3':  # 机械按键3
        if not tkinter_label.var[2]:  # MQTT服务未绑定
            main.PressKey(main.M3)
            print("recieve m3")
        else:
            mqtt_file.Mqtt_send("M3")
    elif ID == '4':  # 机械按键4
        if not tkinter_label.var[3]:  # MQTT服务未绑定
            main.PressKey(main.M4)
        else:
            mqtt_file.Mqtt_send("M4")
    elif ID == 'U':  # 上键
        if not tkinter_label.var[4]:  # MQTT服务未绑定
            main.PressKey(main.Ku)
        else:
            mqtt_file.Mqtt_send("KU")  # MQTT发送
    elif ID == 'D':  # 下键
        if not tkinter_label.var[5]:  # MQTT服务未绑定
            main.PressKey(main.Kd)
        else:
            mqtt_file.Mqtt_send("KD")  # MQTT发送
    elif ID == 'L':  # 左键
        if not tkinter_label.var[6]:  # MQTT服务未绑定
            main.PressKey(main.Kl)
        else:
            mqtt_file.Mqtt_send("KL")  # MQTT发送
    elif ID == 'R':  # 右键
        if not tkinter_label.var[7]:  # MQTT服务未绑定
            main.PressKey(main.Kr)
        else:
            mqtt_file.Mqtt_send("KR")  # MQTT发送
    elif ID == 'S':  # 侧键
        if not tkinter_label.var[8]:  # MQTT服务未绑定
            main.PressKey(main.Sk)
        else:
            mqtt_file.Mqtt_send("KS")  # MQTT发送

    elif ID == 'Z':  # 旋钮1左转
        if not tkinter_label.var[9]:  # MQTT服务未绑定
            # 功能判定
            if tkinter_label.var[10] == tkinter_label.Roller:  # 滚轮模式
                main.Mose_down()  # 滚轮向下
            elif tkinter_label.var[10] == tkinter_label.Roller_key:  # 滚轮+按键
                main.Mouse_Key_down(main.knob1)  # 按键 +向下
            elif tkinter_label.var[10] == tkinter_label.volume:  # 音量控制
                main.voice_down()  # 音量减少
            elif tkinter_label.var[10] == tkinter_label.Music_switch:  # 音乐切换
                main.Music_Last()  # 音乐上一曲
            elif tkinter_label.var[10] == tkinter_label.brightness:  # 亮度控制
                main.Light_down()
        else:
            mqtt_file.Mqtt_send("RZ")  # MQTT发送
    elif ID == 'C':  # 旋钮1右转
        # 功能判定
        if not tkinter_label.var[9]:  # MQTT服务未绑定
            if tkinter_label.var[10] == tkinter_label.Roller:  # 滚轮模式
                main.Mose_up()  # 滚轮向上
            elif tkinter_label.var[10] == tkinter_label.Roller_key:  # 滚轮+按键
                main.Mouse_Key_up(main.knob1)  # 按键 + 向上
            elif tkinter_label.var[10] == tkinter_label.volume:  # 音量控制
                main.voice_up()  # 音量增加
            elif tkinter_label.var[10] == tkinter_label.Music_switch:  # 音乐切换
                main.Music_Next()  # 音乐下一曲
            elif tkinter_label.var[10] == tkinter_label.brightness:  # 亮度控制
                main.Light_up()
        else:
            mqtt_file.Mqtt_send("RC")  # MQTT发送
    elif ID == 'X':  # 旋钮1按下
        # 功能判定
        if not tkinter_label.var[11]:  # MQTT服务未绑定
            if tkinter_label.var[12] == tkinter_label.Key:  # 按键控制
                main.PressKey(main.Kb1p)  # 执行按下按键操作
            elif tkinter_label.var[12] == tkinter_label.play:  # 暂停播放
                main.Music_Pause()  # 音乐暂停
            elif tkinter_label.var[12] == tkinter_label.Mute:  # 音量控制
                main.voice_mute()  # 静音/有声切换
        else:
            mqtt_file.Mqtt_send("RX")  # MQTT发送
    elif ID == 'Q':  # 旋钮1按下左转
        # 功能判定
        if not tkinter_label.var[13]:  # MQTT服务未绑定
            if tkinter_label.var[14] == tkinter_label.Roller:  # 滚轮模式
                main.Mose_down()  # 滚轮向下
            elif tkinter_label.var[14] == tkinter_label.Roller_key:  # 滚轮+按键
                main.Mouse_Key_down(main.knob1rp)  # 按键 + 向上
            elif tkinter_label.var[14] == tkinter_label.volume:  # 音量控制
                main.voice_down()  # 音量减少
                print("voice down")
            elif tkinter_label.var[14] == tkinter_label.Music_switch:  # 音乐切换
                main.Music_Last()  # 音乐上一曲
            elif tkinter_label.var[14] == tkinter_label.brightness:  # 亮度控制
                main.Light_down()
        else:
            mqtt_file.Mqtt_send("RQ")  # MQTT发送
    elif ID == 'W':  # 旋钮1按下右转
        # 功能判定
        if not tkinter_label.var[13]:  # MQTT服务未绑定
            if tkinter_label.var[14] == tkinter_label.Roller:  # 滚轮模式
                main.Mose_up()  # 滚轮向上
            elif tkinter_label.var[14] == tkinter_label.Roller_key:  # 滚轮+按键
                main.Mouse_Key_up(main.knob1rp)  # 按键 + 向下
            elif tkinter_label.var[14] == tkinter_label.volume:  # 音量控制
                main.voice_up()  # 音量增加
                print("voice up")
            elif tkinter_label.var[14] == tkinter_label.Music_switch:  # 音乐切换
                main.Music_Next()  # 音乐下一曲
            elif tkinter_label.var[14] == tkinter_label.brightness:  # 亮度控制
                main.Light_up()  # 亮度控制
        else:
            mqtt_file.Mqtt_send("RW")  # MQTT发送

    elif ID == 'V':  # 旋钮2左转
        # 功能判定
        if not tkinter_label.var[15]:  # MQTT服务未绑定
            if tkinter_label.var[16] == tkinter_label.Roller:  # 滚轮模式
                main.Mose_down()  # 滚轮向上
            elif tkinter_label.var[16] == tkinter_label.Roller_key:  # 滚轮+按键
                main.Mouse_Key_down(main.knob1)  # 按键 + 向上
            elif tkinter_label.var[16] == tkinter_label.volume:  # 音量控制
                main.voice_down()  # 音量增加
            elif tkinter_label.var[16] == tkinter_label.Music_switch:  # 音乐切换
                main.Music_Last()  # 音乐下一曲
            elif tkinter_label.var[16] == tkinter_label.brightness:  # 亮度控制
                main.Light_down()
        else:
            mqtt_file.Mqtt_send("RV")  # MQTT发送
    elif ID == 'N':  # 旋钮2右转
        # 功能判定
        if not tkinter_label.var[15]:  # MQTT服务未绑定
            if tkinter_label.var[16] == tkinter_label.Roller:  # 滚轮模式
                main.Mose_up()  # 滚轮向上
            elif tkinter_label.var[16] == tkinter_label.Roller_key:  # 滚轮+按键
                main.Mouse_Key_up(main.knob1)  # 按键 + 向上
            elif tkinter_label.var[16] == tkinter_label.volume:  # 音量控制
                main.voice_up()  # 音量增加
            elif tkinter_label.var[16] == tkinter_label.Music_switch:  # 音乐切换
                main.Music_Next()  # 音乐下一曲
            elif tkinter_label.var[16] == tkinter_label.brightness:  # 亮度控制
                main.Light_up()
        else:
            mqtt_file.Mqtt_send("RN")  # MQTT发送
    elif ID == 'B':  # 旋钮2按下
        # 功能判定
        if not tkinter_label.var[17]:  # MQTT服务未绑定
            if tkinter_label.var[18] == tkinter_label.Key:  # 按键控制
                main.PressKey(main.Kb1p)  # 执行按下按键操作
            elif tkinter_label.var[18] == tkinter_label.play:  # 暂停播放
                main.Music_Pause()  # 音乐暂停
            elif tkinter_label.var[18] == tkinter_label.Mute:  # 音量控制
                main.voice_mute()  # 静音/有声切换
        else:
            mqtt_file.Mqtt_send("RB")  # MQTT发送
    elif ID == 'G':  # 旋钮2按下左转
        # 功能判定
        if not tkinter_label.var[19]:  # MQTT服务未绑定
            if tkinter_label.var[20] == tkinter_label.Roller:  # 滚轮模式
                main.Mose_down()  # 滚轮向下
            elif tkinter_label.var[20] == tkinter_label.Roller_key:  # 滚轮+按键
                main.Mouse_Key_down(main.knob1rp)  # 按键 + 向上
            elif tkinter_label.var[20] == tkinter_label.volume:  # 音量控制
                main.voice_down()  # 音量减少
                print("voice down")
            elif tkinter_label.var[20] == tkinter_label.Music_switch:  # 音乐切换
                main.Music_Last()  # 音乐上一曲
            elif tkinter_label.var[20] == tkinter_label.brightness:  # 亮度控制
                main.Light_down()
        else:
            mqtt_file.Mqtt_send("RG")  # MQTT发送
    elif ID == 'H':  # 旋钮2按下右转
        # 功能判定
        if not tkinter_label.var[19]:  # MQTT服务未绑定
            if tkinter_label.var[20] == tkinter_label.Roller:  # 滚轮模式
                main.Mose_up()  # 滚轮向上
            elif tkinter_label.var[20] == tkinter_label.Roller_key:  # 滚轮+按键
                main.Mouse_Key_up(main.knob1rp)  # 按键 + 向下
            elif tkinter_label.var[20] == tkinter_label.volume:  # 音量控制
                main.voice_up()  # 音量增加
                print("voice up")
            elif tkinter_label.var[20] == tkinter_label.Music_switch:  # 音乐切换
                main.Music_Next()  # 音乐下一曲
            elif tkinter_label.var[20] == tkinter_label.brightness:  # 亮度控制
                main.Light_up()  # 亮度控制
        else:
            mqtt_file.Mqtt_send("RH")  # MQTT发送
