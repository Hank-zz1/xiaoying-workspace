import winreg
import ctypes

TARGET_EXE = "ClipboardOCRV2.exe"
TRAY_KEY_PATH = r"Control Panel\NotifyIconSettings"

def set_tray_always_visible(exe_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, TRAY_KEY_PATH)
        num_subkeys = winreg.QueryInfoKey(key)[0]
        found = False
        for i in range(num_subkeys):
            subkey_name = winreg.EnumKey(key, i)
            subkey = winreg.OpenKey(key, subkey_name, 0, winreg.KEY_READ)
            num_values = winreg.QueryInfoKey(subkey)[1]
            all_values = {}
            for j in range(num_values):
                name, value, vtype = winreg.EnumValue(subkey, j)
                if name != "IconSnapshot":
                    all_values[name] = value
            exe = str(all_values.get("ExecutablePath", ""))
            winreg.CloseKey(subkey)
            if exe_name.lower() in exe.lower():
                subkey_w = winreg.OpenKey(key, subkey_name, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(subkey_w, "IsPromoted", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(subkey_w)
                print("已设置 IsPromoted=1 for " + exe)
                found = True
        winreg.CloseKey(key)
        return found
    except FileNotFoundError:
        print("注册表路径不存在: " + TRAY_KEY_PATH)
        return False

def refresh_tray():
    """通过Windows API广播设置变更消息刷新托盘，不杀explorer进程"""
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    result = ctypes.c_ulong()
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, None,
        SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
    )

def main():
    print("正在设置 ClipboardOCRV2 托盘图标始终显示...")
    found = set_tray_always_visible(TARGET_EXE)
    if not found:
        print("未在注册表中找到 " + TARGET_EXE + " 的托盘图标记录")
        return False
    print("正在刷新托盘区域...")
    refresh_tray()
    print("设置完成！如托盘图标未立即显示，请注销重新登录或重启电脑。")
    return True

if __name__ == "__main__":
    main()
