#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import tkinter as tk
from tkinter import ttk
import serial_file
import tkinter.font as tf  # 引入字体库
import configparser  # 读取配置文件
import main
import mqtt_file  # MQTT服务函数
import tkinter.messagebox  # 异常弹窗库



# 宏定义
PageCom = 1  # 串口配置页
PageFile = 2  # 预设配置页
PageKey = 3  # 按键配置页
PageKnob = 4  # 旋钮配置页
PageMqtt = 5  # MQTT配置页
Pageshow = 6  # 说明页
LstPage = 1

first_flag = [0, 0, 0, 0, 0, 0]  # 串口  预设 按键 label MQTT 预设
error_flag = [0, 0]  # 读取文件异常
var = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # tkinter变量的数组
# 主要框架
def BaseDesk(root):
    root.title('多功能小键盘')  # 设置标题
    root.geometry("600x600")  # 设置尺寸
    root.resizable(False, False)  # 不拉伸
    Menu_init(root)


# 侧边栏
def Menu_init(self):

    self.menuinit = tk.Frame(self.master, width=64, height=750, bg="white")
    self.menuinit.place(x=0, y=0)

    # 串口按键
    filename = main.ABSPATH + "\img\com.png"
    pic_com = tk.PhotoImage(file=filename)
    icon_com = tk.Button(self.menuinit, text="串口设置", compound="top", image=pic_com, cursor='draped_box',
                         command=lambda: ButtonChange(PageCom))
    icon_com.image = pic_com  # 很重要保持引用
    icon_com.place(x=0, y=0)  # 串口按钮位置属性

    # 预设按键
    filename = main.ABSPATH + r"\img\text.png"
    pic_text = tk.PhotoImage(file=filename)
    icon_text = tk.Button(self.menuinit, text="预设设置", compound="top", image=pic_text, cursor='draped_box',
                          command=lambda: ButtonChange(PageFile))
    icon_text.image = pic_text  # 很重要保持引用
    icon_text.place(x=-5, y=92)  # 预设按钮位置属性

    # 键盘按键
    filename = main.ABSPATH + r"\img\keyboard.png"
    pic_keyport = tk.PhotoImage(file=filename)
    icon_keyport = tk.Button(self.menuinit, text="键盘设置", compound="top", image=pic_keyport, cursor='draped_box',
                             command=lambda: ButtonChange(PageKey))
    icon_keyport.image = pic_keyport  # 很重要保持引用
    icon_keyport.place(x=-3, y=92*2)  # 键盘按钮位置属性

    # 旋钮按键
    filename = main.ABSPATH + r"\img\knob.png"
    pic_knob = tk.PhotoImage(file=filename)
    icon_mqtt = tk.Button(self.menuinit, text="旋钮设置", compound="top", image=pic_knob, cursor='draped_box',
                          command=lambda: ButtonChange(PageKnob))
    icon_mqtt.image = pic_knob  # 很重要保持引用
    icon_mqtt.place(x=-2, y=92 * 3)  # 旋钮按钮位置属性

    # MQTT按键
    filename = main.ABSPATH + r"\img\mqtt.png"
    pic_mqtt = tk.PhotoImage(file=filename)
    icon_mqtt = tk.Button(self.menuinit, text="MQTT设置", compound="top", image=pic_mqtt, cursor='draped_box',
                          command=lambda: ButtonChange(PageMqtt))
    icon_mqtt.image = pic_mqtt  # 很重要保持引用
    icon_mqtt.place(x=-2, y=92*4)  # MQTT按钮位置属性

    ButtonChange(PageCom)


# 串口页
def com_init(self):
    global first_flag
    global tip_str, button_var, varPort, combo_com

    # 串口状态显示
    text = tf.Font(family='楷体', size=20)  # 设置字体
    label_com = tk.Label(self, text="串口号", font=text, bg="grey")
    label_com.place(x=0, y=50)

    # 串口状态指示
    if first_flag[0] == 0:
        # tip_str = tk.StringVar()
        #
        # varPort = tk.StringVar()
        # button_var = tk.StringVar()
        first_flag[0] = 1  # 清除第一次打开标志位

    tip_str.set("请选择串口")
    label_tip = tk.Label(self, textvariable=tip_str, font=text, bg="grey")
    label_tip.place(x=0, y=100)

    # 串口下拉框
    combo_com = ttk.Combobox(self, textvariable=varPort, font=text, justify=tk.CENTER)
    serial_com = serial_file.GetCom(self)
    combo_com['values'] = serial_com
    combo_com.place(x=100, y=50)

    button_var.set("打开串口")
    buttonOpenCom = tk.Button(self, textvariable=button_var, font=text)
    buttonOpenCom.bind("<Button-1>", lambda event: serial_file.usart_open(combo_com.get(), tip_str, button_var))
    buttonOpenCom.place(x=410, y=45)

    # 串口搜索按钮
    button_sea = tk.StringVar()
    button_sea.set("搜索")
    buttonSearchCom = tk.Button(self, textvariable=button_sea, font=text)
    buttonSearchCom.bind("<Button-1>", lambda event: serial_file.GetCom(self))
    buttonSearchCom.place(x=410, y=95)



# 串口列表刷新
def com_refresh(self, com):
    global combo_com
    combo_com['values'] = com

# 预设页
def file_init(self):
    global file_value

    text = tf.Font(family='楷体', size=20)  # 设置字体
    label_com = tk.Label(self, text="预设选择：", font=text, bg="grey").place(x=0, y=0)
    # print(file_value.get())
    tk.Radiobutton(self, text="PR预设", value=1, font=text, bg="grey", variable=file_value,
                   command=lambda: fileupdata(file_value.get())).place(x=0, y=60)
    tk.Radiobutton(self, text="PS预设", value=2, font=text, bg="grey", variable=file_value,
                   command=lambda: fileupdata(file_value.get())).place(x=0, y=120)
    tk.Radiobutton(self, text="立创预设", value=3, font=text, bg="grey", variable=file_value,
                   command=lambda: fileupdata(file_value.get())).place(x=0, y=180)
    tk.Radiobutton(self, text="自定义预设", value=4, font=text, bg="grey", variable=file_value,
                   command=lambda: fileupdata(file_value.get())).place(x=0, y=240)


# 键盘预设更新函数
def fileupdata(ID):
    global error_flag  # 错误标志位
    global filename
    error_flag[0] = 0

    # filename = ""  # 文件地址
    if ID == 1:  # PR预设
        filename = "\config\prconfig.ini"
        print("PR预设读取")
    elif ID==2:  # PS预设
        filename = "\config\psconfig.ini"
        print("PS预设读取")
    elif ID == 3:  # 立创预设
        filename = "\config\lcconfig.ini"
        print("立创预设读取")
    elif ID == 4:  # 自定义预设
        filename = "\config\selfconfig.ini"
        print("自定义预设读取")
        # dlg = win32ui.CreateFileDialog(1)  # 参数 1 表示打开文件对话框
        # dlg.SetOFNInitialDir('C:/')  # 设置打开文件对话框中的初始显示目录
        # dlg.DoModal()
        # filename = dlg.GetPathName()  # 返回选择的文件路径和名称
        # if filename != "":  # 返回地址不为空
        #     # 将自定义预设地址写入ini配置
        #     conf = configparser.ConfigParser()
        #     conf.read("./config/softconfig.ini", encoding='utf-8')  # 读取配置保存
        #     conf.set("file", "file", str(filename))  # 将配置写入
        #     conf.write(open("./config/softconfig.ini", "r+"))

    main.Read_Allini(filename)  # 读取指定位置的配置数据

    conf = configparser.ConfigParser()
    filename1 = main.ABSPATH + r"\config\softconfig.ini"
    conf.read(filename1, encoding='utf-8')  # 读取软件配置保存
    conf.set("file", "fileid", str(ID))  # 将软件配置写入
    conf.write(open(filename1, "r+"))


# 根据预设文件读取配置
def file_first_read():
    global file_value, filename
    if first_flag[5] == 0:
        # file_value = tk.IntVar()  # 文件值获取
        first_flag[5] = 1

    if file_value.get() == 1:  # PR预设
        filename = "\config\prconfig.ini"
        main.Read_Allini(filename)
        # print("read pr")
    elif file_value.get() == 2:  # PS预设
        filename = "\config\psconfig.ini"
        main.Read_Allini(filename)
        # print("read ps")
    elif file_value.get() == 3:  # 立创预设
        filename = "\config\lcconfig.ini"
        main.Read_Allini(filename)
        # print("read lc")
    elif file_value.get() == 4:  # 自定义预设
        filename = "\config\selfconfig.ini"
        main.Read_Allini(filename)
        # conf = configparser.ConfigParser()
        # conf.read("./config/softconfig.ini", encoding='utf-8')  # 读取指定位置的配置文件
        # main.Read_Allini(conf.get("file", "file"))  # 获取预设选择



# 键盘页
def key_init(self):
    global filename  # 预设文件名
    filename1 = main.ABSPATH + r"\img\board1.png"
    key_img = tk.PhotoImage(file=filename1)
    imgLabel = tk.Label(self, image=key_img)  # 把图片整合到标签类中
    imgLabel.image = key_img  # 很重要保持引用
    imgLabel.place(x=25, y=340)
    text = tf.Font(family='楷体', size=14)  # 设置字体

    # 机械按键1
    tk.Button(self, text="机械按键1", font=text, bg="grey", command=lambda: keyupdata(main.machine1, self)).place(x=0, y=0)
    # 机械按键2
    tk.Button(self, text="机械按键2", font=text, bg="grey", command=lambda: keyupdata(main.machine2, self)).place(x=275,
                                                                                                              y=0)
    # 机械按键3
    tk.Button(self, text="机械按键3", font=text, bg="grey", command=lambda: keyupdata(main.machine3, self)).place(x=0, y=40)
    # 机械按键4
    tk.Button(self, text="机械按键4", font=text, bg="grey", command=lambda: keyupdata(main.machine4, self)).place(x=275,
                                                                                                              y=40)

    # 上键
    tk.Button(self, text="静音按键上", font=text, bg="grey", command=lambda: keyupdata(main.key_up, self)).place(x=0, y=80)
    # 下
    tk.Button(self, text="静音按键下", font=text, bg="grey", command=lambda: keyupdata(main.key_down, self)).place(x=270,
                                                                                                              y=80)
    # 左
    tk.Button(self, text="静音按键左", font=text, bg="grey", command=lambda: keyupdata(main.key_left, self)).place(x=0,
                                                                                                              y=120)
    # 右
    tk.Button(self, text="静音按键右", font=text, bg="grey", command=lambda: keyupdata(main.key_right, self)).place(x=270,
                                                                                                               y=120)

    # 旋钮1旋转
    tk.Button(self, text="旋钮1旋转", font=text, bg="grey", command=lambda: keyupdata(main.knob1, self)).place(x=0, y=160)
    # 旋钮2旋转
    tk.Button(self, text="旋钮2旋转", font=text, bg="grey", command=lambda: keyupdata(main.knob2, self)).place(x=270, y=160)
    # 旋钮1按下
    tk.Button(self, text="旋钮1按下", font=text, bg="grey", command=lambda: keyupdata(main.knob1, self)).place(x=0, y=200)
    # 旋钮2按下
    tk.Button(self, text="旋钮2按下", font=text, bg="grey", command=lambda: keyupdata(main.knob1, self)).place(x=270, y=200)
    # 旋钮1按下
    tk.Button(self, text="旋钮1按转", font=text, bg="grey", command=lambda: keyupdata(main.knob1, self)).place(x=0, y=240)
    # 旋钮2按下
    tk.Button(self, text="旋钮2按转", font=text, bg="grey", command=lambda: keyupdata(main.knob2, self)).place(x=270, y=240)

    # 侧边按键
    tk.Button(self, text="侧边按键", font=text, bg="grey", command=lambda: keyupdata(main.key_side, self)).place(x=0, y=280)

    # 保存预设按键
    tk.Button(self, text="保存为预设", font=text, bg="white", command=lambda: main.Write_Allini(filename)).place(x=300, y=280)

    labelupdata(self, main.all)  # 按键label所有更新


# 按键label更新函数
def labelupdata(self, keyid):
    global machine1_var, machine2_var, machine3_var, machine4_var, \
        keyup_var, keydown_var, keyleft_var, keyright_var, \
        keyside_var, \
        knob1_var, knob1rp_var, knob1p_var, knob2_var, knob2rp_var, knob2p_var
    text = tf.Font(family='Futura', size=14)  # 设置字体
    # 按键全局变量初始化
    if first_flag[2] == 0:
        # machine1_var = tk.StringVar()  # 机械按键
        # machine2_var = tk.StringVar()
        # machine3_var = tk.StringVar()
        # machine4_var = tk.StringVar()
        # keyup_var = tk.StringVar()  # 静音按键
        # keydown_var = tk.StringVar()
        # keyleft_var = tk.StringVar()
        # keyright_var = tk.StringVar()
        # keyside_var = tk.StringVar()  # 侧边按键
        # knob1_var = tk.StringVar()  # 旋钮1
        # knob2_var = tk.StringVar()  # 旋钮2
        first_flag[2] = 1

    # 局刷
    if keyid == main.machine1:  # 机械1
        machine1_var.set(keytext(main.M1))
        tk.Label(self, text=machine1_var.get(), font=text, bg="white").place(x=110, y=5)
    elif keyid == main.machine2:  # 机械2
        machine2_var.set(keytext(main.M2))
        tk.Label(self, text=machine2_var.get(), font=text, bg="white").place(x=385, y=5)
    elif keyid == main.machine3:  # 机械3
        machine3_var.set(keytext(main.M3))
        tk.Label(self, text=machine3_var.get(), font=text, bg="white").place(x=110, y=45)
    elif keyid == main.machine4:  # 机械4
        machine4_var.set(keytext(main.M4))
        tk.Label(self, text=machine4_var.get(), font=text, bg="white").place(x=385, y=45)
    elif keyid == main.key_up:  # 上
        keyup_var.set(keytext(main.Ku))
        tk.Label(self, text=keyup_var.get(), font=text, bg="white").place(x=120, y=85)
    elif keyid == main.key_down:  # 下
        keydown_var.set(keytext(main.Kd))
        tk.Label(self, text=keydown_var.get(), font=text, bg="white").place(x=390, y=85)
    elif keyid == main.key_left:  # 左
        keyleft_var.set(keytext(main.Kl))
        tk.Label(self, text=keyleft_var.get(), font=text, bg="white").place(x=120, y=125)
    elif keyid == main.key_right:  # 右
        keyright_var.set(keytext(main.Kr))
        tk.Label(self, text=keyright_var.get(), font=text, bg="white").place(x=390, y=125)
    elif keyid == main.key_side: # 侧边
        keyside_var.set(keytext(main.Sk))
        tk.Label(self, text=keyside_var.get(), font=text, bg="white").place(x=120, y=285)
    elif keyid == main.knob1:  # 旋钮1旋转
        knob1_var.set(keytext(main.Kb1))
        tk.Label(self, text=knob1_var.get(), font=text, bg="white").place(x=120, y=165)
    elif keyid == main.knob1rp:  # 旋钮1按下旋转
        knob1rp_var.set(keytext(main.Kb1rp))
        tk.Label(self, text=knob1rp_var.get(), font=text, bg="white").place(x=120, y=245)
    elif keyid == main.knob1p:  # 旋钮1按下
        knob1p_var.set(keytext(main.Kb1p))
        tk.Label(self, text=knob1p_var.get(), font=text, bg="white").place(x=120, y=205)
    elif keyid == main.knob2:  # 旋钮2旋转
        knob2_var.set(keytext(main.Kb2))
        tk.Label(self, text=knob2_var.get(), font=text, bg="white").place(x=390, y=165)
    elif keyid == main.knob2rp:  # 旋钮2按下旋转
        knob2rp_var.set(keytext(main.Kb2rp))
        tk.Label(self, text=knob2rp_var.get(), font=text, bg="white").place(x=390, y=245)
    elif keyid == main.knob2p:  # 旋钮2按下
        knob2p_var.set(keytext(main.Kb2p))
        tk.Label(self, text=knob2p_var.get(), font=text, bg="white").place(x=390, y=205)
    else:  # 全刷
        for i in range(1, main.all):
            labelupdata(self, i)

# 旋钮相关参数
Roller = 1  # 滚轮模式
Roller_key = 2  # 滚轮+按键模式
volume = 3  # 音量控制
Music_switch = 4  # 音乐切换
brightness = 5  # 亮度控制

# 旋钮按键参数
Key = 1  # 普通按键
play = 2  # 播放暂停
Mute = 3  # 静音


# 旋钮页面初始化
def knob_init(self):
    global Roller, Roller_key, volume, Music_switch, brightness, \
        knob1_r_value, knob1_rp_value, knob1_p_value, \
        knob2_r_value, knob2_rp_value, knob2_p_value

    # knob1_r_value = tk.IntVar()
    # knob1_rp_value = tk.IntVar()
    # knob1_p_value = tk.IntVar()
    # knob2_r_value = tk.IntVar()
    # knob2_rp_value = tk.IntVar()
    # knob2_p_value = tk.IntVar()

    text = tf.Font(family='Futura', size=20)  # 设置字体
    tk.Label(self, text="旋钮1", font=text, bg="grey").place(x=0, y=0)
    tk.Label(self, text="旋钮2", font=text, bg="grey").place(x=250, y=0)
    text = tf.Font(family='Futura', size=14)  # 设置字体
    # 旋钮1相关设置
    tk.Label(self, text="正常旋转", font=text, bg="grey").place(x=0, y=50)
    tk.Radiobutton(self, text="鼠标滚轮", variable=knob1_r_value, font=text, bg="grey", value=Roller).place(x=100, y=50)
    tk.Radiobutton(self, text="滚轮+按键", variable=knob1_r_value, font=text, bg="grey", value=Roller_key).place(x=100, y=80)
    tk.Radiobutton(self, text="音量控制", variable=knob1_r_value, font=text, bg="grey", value=volume).place(x=100, y=110)
    tk.Radiobutton(self, text="音乐切换", variable=knob1_r_value, font=text, bg="grey",value=Music_switch).place(x=100, y=140)
    tk.Radiobutton(self, text="亮度控制", variable=knob1_r_value, font=text, bg="grey", value=brightness).place(x=100, y=170)

    tk.Label(self, text="按下旋转", font=text, bg="grey").place(x=0, y=250)
    tk.Radiobutton(self, text="鼠标滚轮", variable=knob1_rp_value, font=text, bg="grey", value=Roller).place(x=100, y=250)
    tk.Radiobutton(self, text="滚轮+按键", variable=knob1_rp_value, font=text, bg="grey", value=Roller_key).place(x=100, y= 280)
    tk.Radiobutton(self, text="音量控制", variable=knob1_rp_value, font=text, bg="grey", value=volume).place(x=100, y= 310)
    tk.Radiobutton(self, text="音乐切换", variable=knob1_rp_value, font=text, bg="grey", value=Music_switch).place(x=100, y= 340)
    tk.Radiobutton(self, text="亮度控制", variable=knob1_rp_value, font=text, bg="grey", value=brightness).place(x=100, y= 370)

    tk.Label(self, text="按下设置", font=text, bg="grey").place(x=0, y=450)
    tk.Radiobutton(self, text="按键", variable=knob1_p_value, font=text, bg="grey", value=Key).place(x=100, y=450)
    tk.Radiobutton(self, text="暂停播放", variable=knob1_p_value, font=text, bg="grey", value=play).place(x=100, y=480)
    tk.Radiobutton(self, text="静音/有声", variable=knob1_p_value, font=text, bg="grey", value=Mute).place(x=100, y=510)

    # 旋钮2相关设置
    tk.Label(self, text="正常旋转", font=text, bg="grey").place(x=250, y=50)
    tk.Radiobutton(self, text="鼠标滚轮", variable=knob2_r_value, font=text, bg="grey", value=Roller).place(x=350, y=50)
    tk.Radiobutton(self, text="滚轮+按键", variable=knob2_r_value, font=text, bg="grey", value=Roller_key).place(x=350, y=80)
    tk.Radiobutton(self, text="音量控制", variable=knob2_r_value, font=text, bg="grey", value=volume).place(x=350, y=110)
    tk.Radiobutton(self, text="音乐切换", variable=knob2_r_value, font=text, bg="grey", value=Music_switch).place(x=350, y=140)
    tk.Radiobutton(self, text="亮度控制", variable=knob2_r_value, font=text, bg="grey", value=brightness).place(x=350, y=170)

    tk.Label(self, text="按下旋转", font=text, bg="grey").place(x=250, y=250)
    tk.Radiobutton(self, text="鼠标滚轮", variable=knob2_rp_value, font=text, bg="grey", value=Roller).place(x=350, y=250)
    tk.Radiobutton(self, text="滚轮+按键", variable=knob2_rp_value, font=text, bg="grey", value=Roller_key).place(x=350, y=280)
    tk.Radiobutton(self, text="音量控制", variable=knob2_rp_value, font=text, bg="grey", value=volume).place(x=350, y=310)
    tk.Radiobutton(self, text="音乐切换", variable=knob2_rp_value, font=text, bg="grey", value=Music_switch).place(x=350, y=340)
    tk.Radiobutton(self, text="亮度控制", variable=knob2_rp_value, font=text, bg="grey", value=brightness).place(x=350, y=370)

    tk.Label(self, text="按下设置", font=text, bg="grey").place(x=250, y=450)
    tk.Radiobutton(self, text="按键", variable=knob2_p_value, font=text, bg="grey", value=Key).place(x=350, y=450)
    tk.Radiobutton(self, text="暂停播放", variable=knob2_p_value, font=text, bg="grey", value=play).place(x=350, y=480)
    tk.Radiobutton(self, text="静音/有声", variable=knob2_p_value, font=text, bg="grey", value=Mute).place(x=350, y=510)


# Mqtt页 复选框
def mqtt_init(self):
    global first_flag, m1_mt_var, m2_mt_var, m3_mt_var, m4_mt_var, \
        ku_mt_var, kd_mt_var, kl_mt_var, kr_mt_var, \
        ks_mt_var, kb1_mt_var, kb2_mt_var, \
        mqtt_status, ip_var, port_var

    text = tf.Font(family='Futura', size=14)  # 设置字体

    if first_flag[4] == 0:
        # m1_mt_var = tk.BooleanVar()  # 机械按键
        # m2_mt_var = tk.BooleanVar()
        # m3_mt_var = tk.BooleanVar()
        # m4_mt_var = tk.BooleanVar()
        # ku_mt_var = tk.BooleanVar()  # 静音按键
        # kd_mt_var = tk.BooleanVar()
        # kl_mt_var = tk.BooleanVar()
        # kr_mt_var = tk.BooleanVar()
        # ks_mt_var = tk.BooleanVar()  # 侧边按键
        # kb1_mt_var = tk.BooleanVar()  # 旋钮1
        # kb2_mt_var = tk.BooleanVar()  # 旋钮2
        # ip_var = tk.StringVar()  # IP地址全局
        # port_var = tk.StringVar()  # IP地址全局
        mqtt_status = tk.StringVar()  # MQTT链接/断开按钮
        mqtt_status.set("链接")
        first_flag[4] = 1

    # MQTT相关设置
    tk.Label(self, text="请输入MQTT IP", font=text, bg="grey").place(x=0, y=0)
    IP = tk.Entry(self, show=None, textvariable=ip_var)  # IP地址输入框
    IP.place(x=150, y=1)

    tk.Label(self, text="请输入MQTT端口", font=text, bg="grey").place(x=0, y=20)
    Port = tk.Entry(self, show=None, textvariable=port_var)
    Port.place(x=150, y=21)  # Port端口输入框

    tk.Button(self, text=mqtt_status.get(), font=text, bg="white",
              command=lambda: mqtt_file.Mqtt_Status(mqtt_status, IP.get(), Port.get(), self)).place(x=300, y=5)

    # 复选框
    tk.Checkbutton(self, text="机械按键1", variable=m1_mt_var, font=text, bg="grey").place(x=0, y=100)  # command=
    tk.Checkbutton(self, text="机械按键2", variable=m2_mt_var, font=text, bg="grey").place(x=0, y=140)  # command=
    tk.Checkbutton(self, text="机械按键3", variable=m3_mt_var, font=text, bg="grey").place(x=0, y=180)  # command=
    tk.Checkbutton(self, text="机械按键4", variable=m4_mt_var, font=text, bg="grey").place(x=0, y=220)  # command=

    tk.Checkbutton(self, text="上", variable=ku_mt_var, font=text, bg="grey").place(x=200, y=100)
    tk.Checkbutton(self, text="下", variable=kd_mt_var, font=text, bg="grey").place(x=200, y=140)
    tk.Checkbutton(self, text="左", variable=kl_mt_var, font=text, bg="grey").place(x=200, y=180)
    tk.Checkbutton(self, text="右", variable=kr_mt_var, font=text, bg="grey").place(x=200, y=220)

    tk.Checkbutton(self, text="旋钮1旋转", variable=kb1_r_mt_var, font=text, bg="grey").place(x=0, y=260)
    tk.Checkbutton(self, text="旋钮1按下旋转", variable=kb1_rp_mt_var, font=text, bg="grey").place(x=0, y=300)
    tk.Checkbutton(self, text="旋钮1按下", variable=kb1_p_mt_var, font=text, bg="grey").place(x=0, y=340)

    tk.Checkbutton(self, text="旋钮2旋转", variable=kb2_r_mt_var, font=text, bg="grey").place(x=200, y=260)
    tk.Checkbutton(self, text="旋钮2按下旋转", variable=kb2_rp_mt_var, font=text, bg="grey").place(x=200, y=300)
    tk.Checkbutton(self, text="旋钮2按下", variable=kb2_p_mt_var, font=text, bg="grey").place(x=200, y=340)

    tk.Checkbutton(self, text="侧边按键", variable=ks_mt_var, font=text, bg="grey").place(x=0, y=380)


# MQTT链接按键 及 链接状态显示
def MQTTStatusUpdata(self):
    global mqtt_status
    text = tf.Font(family='Futura', size=14)  # 设置字体
    tk.Button(self, text=mqtt_status.get(), font=text, bg="white",
              command=lambda: mqtt_file.Mqtt_Status(mqtt_status, " ", 0, self)).place(x=300, y=5)


# 页面刷新函数
def ButtonChange(Page):
    # 将旧画布清空

    clean = tk.Frame(root, width=686, height=750, bg="grey")
    clean.place(x=64, y=0)
    if Page == PageCom:  # 串口界面初始化
        com_init(clean)
    elif Page == PageFile:  # 预设界面初始化
        file_init(clean)
    elif Page == PageKey:  # 键盘页面初始化
        key_init(clean)
    elif Page == PageMqtt:  # MQTT页面初始化
        mqtt_init(clean)
    elif Page == PageKnob:
        knob_init(clean)  # 旋钮页面初始化


# 按键更新函数
def keyupdata(KeyID, self):
    global machine1_var, machine2_var, machine3_var, machine4_var, \
        keyup_var, keydown_var, keyleft_var, keyright_var, \
        keyside_var, \
        knob1_var, knob1rp_var, knob1p_var, knob2_var, knob2rp_var, knob2p_var

    # # 按键全局变量初始化
    # if first_flag[3] == 0:
    #     machine1_var = tk.StringVar()  # 机械按键
    #     machine2_var = tk.StringVar()
    #     machine3_var = tk.StringVar()
    #     machine4_var = tk.StringVar()
    #     keyup_var = tk.StringVar()  # 静音按键
    #     keydown_var = tk.StringVar()
    #     keyleft_var = tk.StringVar()
    #     keyright_var = tk.StringVar()
    #     keyside_var = tk.StringVar()  # 侧边按键
    #     knob1_var = tk.StringVar()  # 旋钮1
    #     knob2_var = tk.StringVar()  # 旋钮2
    #     first_flag[3] = 1

    if KeyID == main.machine1:  # 设定机械键盘1
        # 等待数据
        main.M1 = (main.GetKeyBoard()).copy()
        # 数据更新
        machine1_var.set(keytext(main.M1))
        labelupdata(self, main.machine1)  # 更新机械按键1
    elif KeyID == main.machine2:
        # 等待数据
        main.M2 = (main.GetKeyBoard()).copy()
        # 数据更新
        machine1_var.set(keytext(main.M2))
        labelupdata(self, main.machine2)  # 更新机械按键2
    elif KeyID == main.machine3:
        # 等待数据
        main.M3 = (main.GetKeyBoard()).copy()
        # 数据更新
        machine1_var.set(keytext(main.M3))
        labelupdata(self, main.machine3)  # 更新机械按键3
    elif KeyID == main.machine4:
        # 等待数据
        main.M4 = (main.GetKeyBoard()).copy()
        # 数据更新
        machine1_var.set(keytext(main.M4))
        labelupdata(self, main.machine4)  # 更新机械按键4
    elif KeyID == main.key_up:
        # 等待数据
        main.Ku = (main.GetKeyBoard()).copy()
        # 数据更新
        machine1_var.set(keytext(main.Ku))
        labelupdata(self, main.key_up)  # 更新 上
    elif KeyID == main.key_down:
        # 等待数据
        main.Kd = (main.GetKeyBoard()).copy()
        # 数据更新
        keydown_var.set(keytext(main.Kd))
        labelupdata(self, main.key_down)  # 更新 下
    elif KeyID == main.key_left:
        # 等待数据
        main.Kl = (main.GetKeyBoard()).copy()
        # 数据更新
        keyleft_var.set(keytext(main.Kl))
        labelupdata(self, main.key_left)  # 更新 左
    elif KeyID == main.key_right:
        # 等待数据
        main.Kr = (main.GetKeyBoard()).copy()
        # 数据更新
        keyright_var.set(keytext(main.Kr))
        labelupdata(self, main.key_right)  # 更新 右


# 将按键值转换为字符串
def keytext(key):
    meg = ""
    if int(float(key[3])) == 1:
        meg = str(key[0])
        for i in range(len(meg), 14):
            meg = meg + ' '
        return meg
    elif int(float(key[3])) == 2:
        # return str(main.M1[0]) + '+' + str(main.M1[1])
        meg = str(key[0])+ '+' + str(key[1])
        for i in range(len(meg), 14):
            meg = meg + ' '
        return meg
    elif int(float(key[3])) == 3:
        meg = str(key[0]) + '+' + str(key[1] + '+' + str(key[2]))
        for i in range(len(meg), 14):
            meg = meg + ' '
        return meg



# 系统配置初始化函数
def config_read():  # 配置信息读取 开机时读取
    global file_value, \
    knob1_r_value, knob1_rp_value, knob1_p_value, knob2_r_value, knob2_rp_value, knob2_p_value, \
    ip_var, port_var, m1_mt_var, m2_mt_var, m3_mt_var, m4_mt_var, \
    ku_mt_var, kd_mt_var, kl_mt_var, kr_mt_var, ks_mt_var, \
    kb1_r_mt_var, kb1_rp_mt_var, kb1_p_mt_var, kb2_r_mt_var, kb2_rp_mt_var, kb2_p_mt_var
    filename = main.ABSPATH + "\config\softconfig.ini"
    conf = configparser.ConfigParser()
    conf.read(filename, encoding='utf-8')  # 读取指定位置的配置文件
    # 预设信息获取
    file_value.set(int(conf.get("file", "fileid")))  # 获取预设配置信息

    # 旋钮信息获取
    knob1_r_value.set(int(conf.get("knob", "knob1r")))  # 旋转 获取旋钮配置信息
    knob1_rp_value.set(int(conf.get("knob", "knob1rp")))  # 旋转按下 获取旋钮配置信息
    knob1_p_value.set(int(conf.get("knob", "knob1p")))  # 按下 获取旋钮配置信息
    knob2_r_value.set(int(conf.get("knob", "knob2r")))  # 旋转 获取旋钮配置信息
    knob2_rp_value.set(int(conf.get("knob", "knob2rp")))  # 旋转按下 获取旋钮配置信息
    knob2_p_value.set(int(conf.get("knob", "knob2p")))  # 按下 获取旋钮配置信息

    # MQTT信息获取
    ip_var.set(str(conf.get("mqtt", "ip")))
    port_var.set(str(conf.get("mqtt", "port")))

    m1_mt_var.set(bool(int(conf.get("mqtt", "m1"))))  # 获取机械按键MQTT配置
    m2_mt_var.set(bool(int(conf.get("mqtt", "m2"))))  # 获取机械按键MQTT配置
    m3_mt_var.set(bool(int(conf.get("mqtt", "m3"))))  # 获取机械按键MQTT配置
    m4_mt_var.set(bool(int(conf.get("mqtt", "m4"))))  # 获取机械按键MQTT配置

    ku_mt_var.set(bool(int(conf.get("mqtt", "ku"))))  # 获取静音按键MQTT配置
    kd_mt_var.set(bool(int(conf.get("mqtt", "kd"))))  # 获取静音按键MQTT配置
    kl_mt_var.set(bool(int(conf.get("mqtt", "kl"))))  # 获取静音按键MQTT配置
    kr_mt_var.set(bool(int(conf.get("mqtt", "kr"))))  # 获取静音按键MQTT配置

    ks_mt_var.set(bool(int(conf.get("mqtt", "ks"))))  # 获取侧边按键MQTT配置

    kb1_r_mt_var.set(bool(int(conf.get("mqtt", "kb1"))))  # 获取旋钮旋转MQTT配置
    kb1_rp_mt_var.set(bool(int(conf.get("mqtt", "kb1rp"))))  # 获取旋钮按下旋转MQTT配置
    kb1_p_mt_var.set(bool(int(conf.get("mqtt", "kb1p"))))  # 获取旋钮按下MQTT配置

    kb2_r_mt_var.set(bool(int(conf.get("mqtt", "kb2"))))  # 获取旋钮旋转MQTT配置
    kb2_rp_mt_var.set(bool(int(conf.get("mqtt", "kb2rp"))))  # 获取旋钮按下旋转MQTT配置
    kb2_p_mt_var.set(bool(int(conf.get("mqtt", "kb2p"))))  # 获取旋钮按下MQTT配置
    tk_var()  # 获取变量

# 程序退出函数 将所有数据写入配置文件
def on_closing():
    global file_value, \
    knob1_r_value, knob1_rp_value, knob1_p_value, knob2_r_value, knob2_rp_value, knob2_p_value, \
    ip_var, port_var, m1_mt_var, m2_mt_var, m3_mt_var, m4_mt_var, \
    ku_mt_var, kd_mt_var, kl_mt_var, kr_mt_var, ks_mt_var, \
    kb1_r_mt_var, kb1_rp_mt_var, kb1_p_mt_var, kb2_r_mt_var, kb2_rp_mt_var, kb2_p_mt_var
    filename = main.ABSPATH + "\config\softconfig.ini"
    conf = configparser.ConfigParser()
    conf.read(filename, encoding='utf-8')  # 读取软件配置保存

    # MQTT所有配置信息
    conf.set("mqtt", "ip", str(ip_var.get()))  # 将MQTT配置写入
    conf.set("mqtt", "port", str(port_var.get()))  # 将MQTT配置写入
    # 机械按键
    conf.set("mqtt", "m1", str(booltonum(m1_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "m2", str(booltonum(m2_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "m3", str(booltonum(m3_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "m4", str(booltonum(m4_mt_var.get())))  # 将MQTT配置写入
    # 静音按键
    conf.set("mqtt", "ku", str(booltonum(ku_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "kd", str(booltonum(kd_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "kl", str(booltonum(kl_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "kr", str(booltonum(kr_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "ks", str(booltonum(ks_mt_var.get())))  # 将MQTT配置写入
    # 旋钮 MQTT
    conf.set("mqtt", "kb1", str(booltonum(kb1_r_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "kb1p", str(booltonum(kb1_p_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "kb1rp", str(booltonum(kb1_rp_mt_var.get())))  # 将MQTT配置写入

    conf.set("mqtt", "kb2", str(booltonum(kb2_r_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "kb2p", str(booltonum(kb2_p_mt_var.get())))  # 将MQTT配置写入
    conf.set("mqtt", "kb2rp", str(booltonum(kb2_rp_mt_var.get())))  # 将MQTT配置写入

    # 旋钮状态信息
    conf.set("knob", "knob1r", str(knob1_r_value.get()))  # 旋钮模式写入
    conf.set("knob", "knob1p", str(knob1_p_value.get()))  # 旋钮模式写入
    conf.set("knob", "knob1rp", str(knob1_rp_value.get()))  # 旋钮模式写入
    conf.set("knob", "knob2r", str(knob2_r_value.get()))  # 旋钮模式写入
    conf.set("knob", "knob2p", str(knob2_p_value.get()))  # 旋钮模式写入
    conf.set("knob", "knob2rp", str(knob2_rp_value.get()))  # 旋钮模式写入

    conf.write(open(filename, "r+"))  # 将数据写入

    root.destroy()


# 布尔转数字
def booltonum(boolnum):
    if boolnum == False:
        return 0
    elif boolnum == True:
        return 1


# 异常弹窗
def error_msg(ErrorID):
    if ErrorID == "read error":
        tk.messagebox.showerror('文件错误', '读取错误 请检查文件')
    elif ErrorID == "com error":
        tk.messagebox.showerror('串口错误', '串口错误 请检查串口')
    elif ErrorID == "mqtt error":
        tk.messagebox.showerror('MQTT错误', 'MQTT链接错误 请检查IP和端口')
    elif ErrorID == "publish fail":
        tk.messagebox.showerror('主题失效', 'MQTT发布失败 请检查MQTT链接等')

def tk_var():
    global tip_str, tip_str, button_var, varPort, file_value, filename, key_value, \
        machine1_var, machine2_var, machine3_var, machine4_var, \
        keyup_var, keydown_var, keyleft_var, keyright_var, keyside_var,\
        knob1_var, knob1rp_var, knob1p_var, knob2_var, knob2rp_var, knob2p_var, \
        m1_mt_var, m2_mt_var, m3_mt_var, m4_mt_var, \
        ku_mt_var, kd_mt_var, kl_mt_var, kr_mt_var, ks_mt_var, \
        kb1_r_mt_var, kb1_r_mt_var, kb1_p_mt_var, kb1_rp_mt_var, kb1_rp_mt_var, \
        kb2_r_mt_var, kb2_r_mt_var, kb2_p_mt_var, kb2_rp_mt_var, kb2_rp_mt_var, \
        knob1_r_value, knob1_p_value, knob1_rp_value,\
        knob2_r_value, knob2_p_value, knob2_rp_value, \
        var

    var[0] = m1_mt_var.get()
    var[1] = m2_mt_var.get()
    var[2] = m3_mt_var.get()
    var[3] = m4_mt_var.get()

    var[4] = ku_mt_var.get()
    var[5] = kd_mt_var.get()
    var[6] = kl_mt_var.get()
    var[7] = kr_mt_var.get()
    var[8] = ks_mt_var.get()

    var[9] = kb1_r_mt_var.get()
    var[10] = knob1_r_value.get()

    var[11] = kb1_p_mt_var.get()
    var[12] = knob1_p_value.get()

    var[13] = kb1_rp_mt_var.get()
    var[14] = knob1_rp_value.get()

    var[15] = kb2_r_mt_var.get()
    var[16] = knob2_r_value.get()

    var[17] = kb2_p_mt_var.get()
    var[18] = knob2_p_value.get()

    var[19] = kb2_rp_mt_var.get()
    var[20] = knob2_rp_value.get()

    print(var)


root = tk.Tk()

root.iconbitmap(main.ABSPATH+r"\img\keyboard.ico")
tip_str = tk.StringVar()  # 串口提示信息
button_var = tk.StringVar()  # 打开/关闭串口字符
varPort = tk.StringVar()  # 串口名
file_value = tk.IntVar()  # 预设选择标记
filename = ""  # 预设文件地址
key_value = tk.IntVar()  # 按键选择标记
# 按键全局变量初始化
machine1_var = tk.StringVar()  # 机械按键
machine2_var = tk.StringVar()
machine3_var = tk.StringVar()
machine4_var = tk.StringVar()
keyup_var = tk.StringVar()  # 静音按键
keydown_var = tk.StringVar()
keyleft_var = tk.StringVar()
keyright_var = tk.StringVar()
keyside_var = tk.StringVar()  # 侧边按键
knob1_var = tk.StringVar()  # 旋钮1旋转
knob1rp_var = tk.StringVar()  # 旋钮1按下旋转
knob1p_var = tk.StringVar()  # 旋钮1按下
knob2_var = tk.StringVar()  # 旋钮2旋转
knob2rp_var = tk.StringVar()  # 旋钮1按下旋转
knob2p_var = tk.StringVar()  # 旋钮1按下
# MQTT服务全局变量初始化
m1_mt_var = tk.BooleanVar()  # 机械按键
m2_mt_var = tk.BooleanVar()
m3_mt_var = tk.BooleanVar()
m4_mt_var = tk.BooleanVar()
ku_mt_var = tk.BooleanVar()  # 静音按键
kd_mt_var = tk.BooleanVar()
kl_mt_var = tk.BooleanVar()
kr_mt_var = tk.BooleanVar()
ks_mt_var = tk.BooleanVar()  # 侧边按键
kb1_r_mt_var = tk.BooleanVar()  # 旋钮1 旋转
kb1_rp_mt_var = tk.BooleanVar()  # 旋钮1 按下旋转
kb1_p_mt_var = tk.BooleanVar()  # 旋钮1 按下
kb2_r_mt_var = tk.BooleanVar()  # 旋钮2 旋转
kb2_rp_mt_var = tk.BooleanVar()  # 旋钮2 按下旋转
kb2_p_mt_var = tk.BooleanVar()  # 旋钮2 按下
# 旋钮功能全局变量
knob1_r_value = tk.IntVar()  # 旋转
knob1_rp_value = tk.IntVar()  # 按下旋转
knob1_p_value = tk.IntVar()  # 按下
knob2_r_value = tk.IntVar()
knob2_rp_value = tk.IntVar()
knob2_p_value = tk.IntVar()
# MQTT 链接/断开状态
mqtt_status = tk.StringVar()# MQTT链接/断开按钮
ip_var = tk.StringVar()  # IP地址全局
port_var = tk.StringVar()  # IP地址全局

combo_com = ttk.Combobox()  # 串口列表全局变量
config_read()  # 系统配置信息初始化
file_first_read()  # 初始化 将所有按键信息读入

BaseDesk(root)  # 基础配置刷新

root.protocol("WM_DELETE_WINDOW", on_closing)  # 绑定关闭按键

