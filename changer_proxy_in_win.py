from ctypes import *
from ctypes.wintypes import *
import codecs
import time

LPWSTR = POINTER(WCHAR)
HINTERNET = LPVOID

INTERNET_PER_CONN_PROXY_SERVER = 2
INTERNET_OPTION_REFRESH = 37
INTERNET_OPTION_SETTINGS_CHANGED = 39
INTERNET_OPTION_PER_CONNECTION_OPTION = 75
INTERNET_PER_CONN_PROXY_BYPASS = 3
INTERNET_PER_CONN_FLAGS = 1

class INTERNET_PER_CONN_OPTION(Structure):
    class Value(Union):
        _fields_ = [
            ('dwValue', DWORD),
            ('pszValue', LPWSTR),
            ('ftValue', FILETIME),
        ]

    _fields_ = [
        ('dwOption', DWORD),
        ('Value', Value),
    ]

class INTERNET_PER_CONN_OPTION_LIST(Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('pszConnection', LPWSTR),
        ('dwOptionCount', DWORD),
        ('dwOptionError', DWORD),
        ('pOptions', POINTER(INTERNET_PER_CONN_OPTION)),
    ]

def set_proxy_settings(ip, port, on=True):
    if on:
        setting = create_unicode_buffer(ip+":"+str(port))
    else:
        setting = None

    InternetSetOption = windll.wininet.InternetSetOptionW
    InternetSetOption.argtypes = [HINTERNET, DWORD, LPVOID, DWORD]
    InternetSetOption.restype  = BOOL

    List = INTERNET_PER_CONN_OPTION_LIST()
    Option = (INTERNET_PER_CONN_OPTION * 3)()
    nSize = c_ulong(sizeof(INTERNET_PER_CONN_OPTION_LIST))

    Option[0].dwOption = INTERNET_PER_CONN_FLAGS
    Option[0].Value.dwValue = 10 # PROXY_TYPE_DIRECT Or
    Option[1].dwOption = INTERNET_PER_CONN_PROXY_SERVER
    Option[1].Value.pszValue = setting
    Option[2].dwOption = INTERNET_PER_CONN_PROXY_BYPASS

    List.dwSize = sizeof(INTERNET_PER_CONN_OPTION_LIST)
    List.pszConnection = None
    List.dwOptionCount = 3
    List.dwOptionError = 0
    List.pOptions = Option

    InternetSetOption(None, INTERNET_OPTION_PER_CONNECTION_OPTION, byref(List), nSize)
    InternetSetOption(None, INTERNET_OPTION_SETTINGS_CHANGED, None, 0)
    InternetSetOption(None, INTERNET_OPTION_REFRESH, None, 0)

def get_proxy():
    f = codecs.open("proxy.txt", "r", "utf-8")
    str_proxy = f.read()
    proxy = str_proxy.split("\n")
    list_proxy = []
    for prox in proxy:
        list_proxy.append(prox.split(":"))
    return list_proxy

def main():
    while True:
        proxys = get_proxy()
        for proxy in proxys:
            print("Пожалуйста, нажмите ENTER для запуска следующего прокси.", end = " ")
            inp = input()
            try:
                set_proxy_settings(ip=proxy[0], port=int(proxy[1]))
            except:
                print("Смена прокси не удалась. ")
                continue
            print("PROXY : " + str(proxy[0] + ":" + proxy[1]))
            time.sleep(5)


if __name__ == '__main__':
    main()