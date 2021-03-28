#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import tkinter_label  # UI界面
import keyboard  # 键盘操作库
import re  # 特定字符串截取
import configparser  # 读取配置文件
import os  # 系统库
import screen_brightness_control  # 系统亮度windows + linux调节
import pyautogui  # 鼠标滚轮操作
import copy  # 列表复制库
from ctypes import cast, POINTER  # 音量相关
from comtypes import CLSCTX_ALL  # 音量相关
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # 音量相关
import sys  # 路径获取
from TrayIcon import _Main# 窗口最小化

print(sys.path)

ABSPATH = os.path.abspath(sys.argv[0])  # main文件绝对路径
ABSPATH = os.path.dirname(ABSPATH)  # 获取除main路径



light_step = 5  # 亮度调整差值
voice_step = 2  # 声音调整差值

machine1 = 1  # 机械按键1
machine2 = 2  # 机械按键2
machine3 = 3  # 机械按键3
machine4 = 4  # 机械按键4

key_up = 5  # 上按键
key_down = 6  # 下按键
key_left = 7  # 左按键
key_right = 8  # 右按键

key_side = 9  # 侧边按键

knob1 = 10  # 旋钮1旋转
knob1rp = 11  # 旋钮1按下旋转
knob1p = 12  # 旋钮1旋转

knob2 = 13  # 旋钮2旋转
knob2rp = 14  # 旋钮2按下旋转
knob2p = 15  # 旋钮2旋转

all = 16  # 全刷

# 规定所有列表的前3位为键值 第四位为键数
M1 = []  # 机械按键1
M2 = []  # 机械按键2
M3 = []  # 机械按键3
M4 = []  # 机械按键4

Ku = []  # 上按键
Kd = []  # 下按键
Kl = []  # 左按键
Kr = []  # 右按键

Sk = []  # 侧边按键

Kb1 = []  # 旋钮1旋转键值
Kb1rp = []  # 旋钮1按下旋转键值
Kb1p = []  # 旋钮1按下键值

Kb2 = []  # 旋钮2旋转键值
Kb2rp = []  # 旋钮2按下旋转键值
Kb2p = []  # 旋钮2按下键值

Music_last = []  # 上一曲
Music_next = []  # 下一曲
Music_pause = []  # 暂停

# 配置名列表
ini_section = [0, 'machine1', 'machine2', 'machine3', 'machine4', 'key_up', 'key_down', 'key_left', 'key_right',
               'key_side', "knob1", "knob1rp", "knob1p", "knob2", "knob2rp", "knob2p"]

# music配置名
music_section = ['music_last', 'music_next', 'music_pause']  # 音乐文件
# 配置文件的路径
conf_path = os.path.dirname(os.path.realpath(__file__)) + "/config/config.ini"


# 音量相关
Volume_dic = {0: -65.25, 1: -56.99, 2: -51.67, 3: -47.74, 4: -44.62, 5: -42.03, 6: -39.82, 7: -37.89, 8: -36.17, 9: -34.63, 10: -33.24,
 11: -31.96, 12: -30.78, 13: -29.68, 14: -28.66, 15: -27.7, 16: -26.8, 17: -25.95, 18: -25.15, 19: -24.38, 20: -23.65,
 21: -22.96, 22: -22.3, 23: -21.66, 24: -21.05, 25: -20.46, 26: -19.9, 27: -19.35, 28: -18.82, 29: -18.32, 30: -17.82,
 31: -17.35, 32: -16.88, 33: -16.44, 34: -16.0, 35: -15.58, 36: -15.16, 37: -14.76, 38: -14.37, 39: -13.99, 40: -13.62,
 41: -13.26, 42: -12.9, 43: -12.56, 44: -12.22, 45: -11.89, 46: -11.56, 47: -11.24, 48: -10.93, 49: -10.63, 50: -10.33,
 51: -10.04, 52: -9.75, 53: -9.47, 54: -9.19, 55: -8.92, 56: -8.65, 57: -8.39, 58: -8.13, 59: -7.88, 60: -7.63,
 61: -7.38, 62: -7.14, 63: -6.9, 64: -6.67, 65: -6.44, 66: -6.21, 67: -5.99, 68: -5.76, 69: -5.55, 70: -5.33,
 71: -5.12, 72: -4.91, 73: -4.71, 74: -4.5, 75: -4.3, 76: -4.11, 77: -3.91, 78: -3.72, 79: -3.53, 80: -3.34,
 81: -3.15, 82: -2.97, 83: -2.79, 84: -2.61, 85: -2.43, 86: -2.26, 87: -2.09, 88: -1.91, 89: -1.75, 90: -1.58,
 91: -1.41, 92: -1.25, 93: -1.09, 94: -0.93, 95: -0.77, 96: -0.61, 97: -0.46, 98: -0.3, 99: -0.15, 100: 0.0}

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def Voice_get(value):
    value = round(value, 2)
    # print(value)
    if value in Volume_dic.values():
        return list(Volume_dic.keys())[list(Volume_dic.values()).index(value)]
    else:
        return 0


Voice_set = 0

mute_flag = 1  # 静音/有声切换标志位 初始为有声1


def voice_config(voice):
    volume.SetMasterVolumeLevel(Volume_dic[voice], None)


# 音量增加
def voice_up():
    global Voice_set, voice_step
    Voice_set = Voice_set + voice_step
    if Voice_set >= 100:
        Voice_set = 100
    # print(Voice_set)
    voice_config(Voice_set)


# 音量减少
def voice_down():
    global Voice_set, voice_step
    Voice_set = Voice_set - voice_step
    if Voice_set <= 0:
        Voice_set = 0
    # print(Voice_set)
    voice_config(Voice_set)


# 音量 静音反转
def voice_mute():
    global mute_flag
    if mute_flag == 1:  # 有声变无声
        mute_flag = 0
        voice_config(0)
        print(mute_flag)
        print(Voice_set)
    elif mute_flag == 0:  # 无声变有声
        mute_flag = 1
        voice_config(Voice_set)  # 恢复原音量
        print(mute_flag)
        print(Voice_set)


# 滚轮向上滚动
def Mose_up():
    pyautogui.scroll(100)


# 滚轮向下滚动
def Mose_down():
    pyautogui.scroll(-100)


# 滚轮+按键 向上
def Mouse_Key_up(KeyID):
    KeyAction = [0, 0, 0, 0]
    if KeyID == knob1:  # 旋钮1旋转
        KeyAction = copy.copy(Kb1)
    elif KeyID == knob1rp:
        KeyAction = copy.copy(Kb1rp)
    elif KeyID == knob2:
        KeyAction = copy.copy(Kb2)
    elif KeyID == knob2rp:
        KeyAction = copy.copy(Kb2rp)

    keyboard.press(KeyAction[0])
    pyautogui.scroll(100)
    keyboard.release(KeyAction[0])


# 滚轮+按键 向下
def Mouse_Key_down(KeyID):
    KeyAction = [0, 0, 0, 0]
    if KeyID == knob1:  # 旋钮1旋转
        KeyAction = copy.copy(Kb1)
    elif KeyID == knob1rp:
        KeyAction = copy.copy(Kb1rp)
    elif KeyID == knob2:
        KeyAction = copy.copy(Kb2)
    elif KeyID == knob2rp:
        KeyAction = copy.copy(Kb2rp)

    keyboard.press(KeyAction[0])
    pyautogui.scroll(-100)
    keyboard.release(KeyAction[0])

Light_set = screen_brightness_control.get_brightness()  # 获取全局亮度

# 调整屏幕亮度
def ScreenChange(percent):
    print(percent)
    screen_brightness_control.fade_brightness(percent, interval=0.01)  # 设置亮度


# 亮度调整函数
def LightConfig(light_num):
    # 限幅函数
    if light_num < 0:
        light_num = 0
    elif light_num > 100:
        light_num = 100
    # 亮度调整函数
    ScreenChange(light_num)


def Light_up():  # 亮度增加函数
    global Light_set, light_step
    Light_set = Light_set + light_step
    if Light_set > 100:
        Light_set = 100
    ScreenChange(Light_set)


def Light_down():  # 亮度减少函数
    global Light_set, light_step
    Light_set = Light_set - light_step
    if Light_set < 0:
        Light_set = 0
    print(Light_set)
    LightConfig(Light_set)  # 进行亮度调节


# 执行音乐上一曲函数
def Music_Last():
    PressKey(Music_last)


# 执行音乐暂停函数
def Music_Pause():
    PressKey(Music_pause)


# 执行音乐下一曲函数
def Music_Next():
    PressKey(Music_next)


# 读取音乐配置文件
def Read_musicData(ID):
    global ABSPATH
    Data = ['0', '0', '0', '0']  # 初始化一个列表
    conf = configparser.ConfigParser()
    filename = ABSPATH + "\config\music.ini"
    # print(filename)
    # conf.read("./config/music.ini", encoding='utf-8')  # 读取指定位置的配置文件
    conf.read(filename, encoding='utf-8')  # 读取指定位置的音乐配置文件
    try:
        Data[0] = conf.get(str(music_section[ID]), "Data0")  # 获取键值1
        Data[1] = conf.get(str(music_section[ID]), "Data1")  # 获取键值2
        Data[2] = conf.get(str(music_section[ID]), "Data2")  # 获取键值3
        Data[3] = conf.get(str(music_section[ID]), "Data3")  # 获取按键数量
    except Exception as e:  # 万能异常
        # if tkinter_label.error_flag[0] == 0:
        #     tkinter_label.error_flag[0] = 1  # 触发异常
        #     tkinter_label.error_msg("music error")  # 抛出异常
        # else:
        #     pass
        print("music error")
        pass
    print(Data)
    return Data  # 将列表返回


# 读取ini节点
def Read_iniData(KeyId, file):
    global ABSPATH
    Data = ['0', '0', '0', '0']  # 初始化一个列表
    conf = configparser.ConfigParser()
    filename = ABSPATH + str(file)
    # print(filename)
    conf.read(filename, encoding='utf-8')  # 读取指定位置的配置文件
    try:
        Data[0] = conf.get(str(ini_section[KeyId]), "data0")  # 获取键值1
        Data[1] = conf.get(str(ini_section[KeyId]), "data1")  # 获取键值2
        Data[2] = conf.get(str(ini_section[KeyId]), "data2")  # 获取键值3
        Data[3] = conf.get(str(ini_section[KeyId]), "data3")  # 获取按键数量
    except Exception as e:  # 万能异常
        if tkinter_label.error_flag[0] == 0:
            tkinter_label.error_flag[0] = 1  # 触发异常
            tkinter_label.error_msg("read error")  # 抛出异常
        else:
            pass
    return Data  # 将列表返回


# 读取配置文件 KeyId要读取的按键 congfigid要读取的存档文件
def Read_ini(KeyId, file):
    global M1, M2, M3, M4, Ku, Kd, Kl, Kr, Sk, \
        Kb1, Kb1rp, Kb1p, Kb2, Kb2rp, Kb2p

    if KeyId == machine1:  # 机械1
        M1 = Read_iniData(KeyId, file)
    elif KeyId == machine2:  # 机械2
        M2 = Read_iniData(KeyId, file)
    elif KeyId == machine3:  # 机械3
        M3 = Read_iniData(KeyId, file)
    elif KeyId == machine4:  # 机械4
        M4 = Read_iniData(KeyId, file)

    elif KeyId == key_up:  # 按键上
        Ku = Read_iniData(KeyId, file)
    elif KeyId == key_down:  # 按键下
        Kd = Read_iniData(KeyId, file)
    elif KeyId == key_left:  # 按键左
        Kl = Read_iniData(KeyId, file)
    elif KeyId == key_right:  # 按键右
        Kr = Read_iniData(KeyId, file)

    elif KeyId == key_side:  # 侧边按键
        Sk = Read_iniData(KeyId, file)

    elif KeyId == knob1:  # 旋钮1旋转
        Kb1 = Read_iniData(KeyId, file)
    elif KeyId == knob1rp:  # 旋钮1按下旋转
        Kb1rp = Read_iniData(KeyId, file)
    elif KeyId == knob1p:  # 旋钮1按下
        Kb1p = Read_iniData(KeyId, file)

    elif KeyId == knob2:  # 旋钮2旋转
        Kb2 = Read_iniData(KeyId, file)
    elif KeyId == knob2rp:  # 旋钮2按下旋转
        Kb2rp = Read_iniData(KeyId, file)
    elif KeyId == knob2p:  # 旋钮2按下
        Kb2p = Read_iniData(KeyId, file)


# 将所有按键信息读入 file 文件地址
def Read_Allini(file):
    global Music_last, Music_next, Music_pause
    for i in range(all):  # 侧边按键最后
        Read_ini(i, file)  # 从配置1读取所有按键数据

    Music_last = Read_musicData(0)  # 读取音乐配置
    Music_next = Read_musicData(1)  # 读取音乐配置
    Music_pause = Read_musicData(2)  # 读取音乐配置
    # print(Music_next)


# 写入ini节点
def Write_iniData(KeyId, file, Key):
    global ABSPATH
    conf = configparser.ConfigParser()
    filename = ABSPATH + str(file)
    conf.read(str(filename), encoding='utf-8')  # 读取指定位置的配置文件

    conf.set(str(ini_section[KeyId]), "data0", str(Key[0]))  # 将所有数据写入
    conf.set(str(ini_section[KeyId]), "data1", str(Key[1]))
    conf.set(str(ini_section[KeyId]), "data2", str(Key[2]))
    conf.set(str(ini_section[KeyId]), "data3", str(Key[3]))

    conf.write(open(str(filename), "r+"))


# 将数据写入对应配置文件 KeyId要写入的按键 congfigid要写入的存档文件
def Write_ini(KeyId, file):
    global M1, M2, M3, M4, Ku, Kd, Kl, Kr, Sk, \
        Kb1, Kb1rp, Kb1p, Kb2, Kb2rp, Kb2p

    # 机械1
    if KeyId == machine1:
        Write_iniData(KeyId, file, M1)
    elif KeyId == machine2:  # 机械2
        Write_iniData(KeyId, file, M2)
    elif KeyId == machine3:  # 机械3
        Write_iniData(KeyId, file, M3)
    elif KeyId == machine4:  # 机械4
        Write_iniData(KeyId, file, M4)

    elif KeyId == key_up:  # 按键上
        Write_iniData(KeyId, file, Ku)
    elif KeyId == key_down:  # 按键下
        Write_iniData(KeyId, file, Kd)
    elif KeyId == key_left:  # 按键左
        Write_iniData(KeyId, file, Kl)
    elif KeyId == key_right:  # 按键右
        Write_iniData(KeyId, file, Kr)

    elif KeyId == key_side:  # 侧边按键
        Write_iniData(KeyId, file, Sk)

    elif KeyId == knob1:  # 旋钮1旋转
        Write_iniData(KeyId, file, Kb1)
    elif KeyId == knob1rp:  # 旋钮1按下旋转
        Write_iniData(KeyId, file, Kb1rp)
    elif KeyId == knob1p:  # 旋钮1按下
        Write_iniData(KeyId, file, Kb1p)

    elif KeyId == knob2:  # 旋钮2旋转
        Write_iniData(KeyId, file, Kb2)
    elif KeyId == knob2rp:  # 旋钮2按下旋转
        Write_iniData(KeyId, file, Kb2rp)
    elif KeyId == knob2p:  # 旋钮2按下
        Write_iniData(KeyId, file, Kb2p)


# 将所有数据写入ini file 写入文件
def Write_Allini(file):
    for i in range(all):  # 所有最后
        Write_ini(i, file)  # 将所有数据写入ini


# 将键值数据写入对应列表
def KeyData(Key,len,KeyID):
    global M1, M2, M3, M4, Ku, Kd, Kl, Kr, Sk, \
        Kb1, Kb1rp, Kb1p, Kb2, Kb2rp, Kb2p

    if KeyID == machine1:  # 机械1
        M1 = Key.copy()
        M1[3] = len
    elif KeyID == machine2:  # 机械2
        M2 = Key.copy()
        M2[3] = len
    elif KeyID == machine3:  # 机械3
        M3 = Key.copy()
        M3[3] = len
    elif KeyID == machine4:  # 机械4
        M4 = Key.copy()
        M4[3] = len

    elif KeyID == key_up:  # 按键上
        Ku = Key.copy()
        Ku[3] = len
    elif KeyID == key_down:  # 按键下
        Kd = Key.copy()
        Kd[3] = len
    elif KeyID == key_left:  # 按键左
        Kl = Key.copy()
        Kl[3] = len
    elif KeyID == key_right:  # 按键右
        Kr = Key.copy()
        Kr[3] = len

    elif KeyID == key_side:  # 侧边按键
        Sk = Key.copy()
        Sk[3] = len

    elif KeyID == knob1:  # 旋钮1
        kb1 = Key.copy()
        kb1[3] = len
    elif KeyID == knob1rp:  # 旋钮1旋转按下
        Kb1rp = Key.copy()
        Kb1rp[3] = len
    elif KeyID == knob1p:  # 旋钮1按下
        Kb1p = Key.copy()
        Kb1p[3] = len

    elif KeyID == knob2:  # 旋钮2
        kb2 = Key.copy()
        kb2[3] = len
    elif KeyID == knob2rp:  # 旋钮2旋转按下
        Kb2rp = Key.copy()
        Kb1rp[3] = len
    elif KeyID == knob2p:  # 旋钮2按下
        Kb2p = Key.copy()
        Kb2p[3] = len


# 执行按键操作 传入按键和操作按键
def PressKey(KeyAction):
    print(KeyAction)  # 显示下键值
    KeyAction[3] = int(float(KeyAction[3]))
    if KeyAction[3] == '1' or KeyAction[3] == 1:
        keyboard.press(KeyAction[1])
        keyboard.release(KeyAction[0])
    elif KeyAction[3] == '2' or KeyAction[3] == 2:
        keyboard.press(KeyAction[0])
        keyboard.press(KeyAction[1])
        keyboard.release(KeyAction[0])
        keyboard.release(KeyAction[1])
    elif KeyAction[3] == '3' or KeyAction[3] == 3:
        keyboard.press(KeyAction[0])
        keyboard.press(KeyAction[1])
        keyboard.press(KeyAction[2])
        keyboard.release(KeyAction[0])
        keyboard.release(KeyAction[1])
        keyboard.release(KeyAction[2])
    else:
        print("error")
        return 0


# 获取要设置的快捷键
def GetKeyBoard():
    KeyPress = []
    keylen = 0
    recorded = keyboard.record(until='esc')  # 等待按键执行完毕
    keystr = [str(i) for i in recorded]  # 将记录的值转换为字符串
    # print(keystr)  # 打印当前按键
    for i in keystr:
        KeyPress.append(re.findall(r"[(](.*?)[ ]", i)[0])  # 取出'('和' ' 内数据
    print(KeyPress)  # 打印原始键值
    # print(len(KeyPress))  # 打印长度
    # 按键数量计算
    if len(KeyPress) % 2 == 1:
        keylen = (len(KeyPress) - 1)/2  # 计算一下快捷键的长度
    elif len(KeyPress) % 2 == 0:
        keylen = len(KeyPress)/2

    for i in range(len(KeyPress), 4):  # 补足4个列表
        KeyPress.append(0)

    KeyPress[3] = int(keylen)

    # print(KeyPress[3])  # 打印按键数量

    if KeyPress[3] == 1:
        KeyPress[1] = 0
        KeyPress[2] = 0
    elif KeyPress[3] == 2:
        KeyPress[2] = 0

    # print(KeyPress)  # 打印按键

    return KeyPress[0:4]

# 运行入口主函数
if __name__ == '__main__':
    # print(ABSPATH)
    # Main = TrayIcon._Main()
    Main = _Main()
    Main.main(tkinter_label.root)
    Voice_get(volume.GetMasterVolumeLevel())  # 获取当前音量值
