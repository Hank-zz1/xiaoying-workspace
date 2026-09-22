---
name: 截图OCR工具
description: 截图OCR工具。首次使用需部署（AI自动完成，约3-8分钟）。部署后桌面生成"截图OCR"快捷方式，双击打开即可使用。打开后桌面右下角托盘图标显示绿色小球表示OCR已开启，按Ctrl+Shift+Z用iHaier截图或Ctrl+Shift+X用Windows截图，自动OCR识别文字并复制到剪贴板，Ctrl+V粘贴。右键托盘可开关OCR、设开机自启、查看使用说明。
icon: 🚀
---

# 截图OCR工具

## 使用方法

**首次使用需先部署**：AI会自动完成部署（复制程序、写入配置、创建快捷方式），约3-8分钟，需用户同意后执行。

部署完成后，程序默认开启（桌面右下角托盘显示绿色小球）。按快捷键截图后自动OCR识别文字，结果复制到剪贴板，Ctrl+V即可粘贴。

**快捷键：**
- `Ctrl+Shift+Z` — iHaier截图+OCR（模拟Ctrl+Shift+A，需iHaier开启）
- `Ctrl+Shift+X` — Windows截图+OCR（模拟Win+Shift+S）
- `Ctrl+Shift+P` — 开关OCR（桌面右下角托盘图标绿色=开/灰色=关）
- `Ctrl+V` — 粘贴识别出的文字

**右键托盘菜单：** 使用说明 / 开机自启 / 退出

**使用流程：**
1. 双击桌面「截图OCR」图标打开程序（桌面右下角托盘显示绿色小球表示已开启）
2. 按 `Ctrl+Shift+Z`（iHaier开启时）或 `Ctrl+Shift+X` 截图
3. 框选屏幕区域，OCR自动识别，结果复制到剪贴板
4. Ctrl+V粘贴文字
5. 右键托盘→开机自启：开启后重启电脑自动启动
6. 右键托盘→退出：关闭程序

## 首次部署检查清单

当用户首次使用此技能时，先告知用户：

**截图OCR工具部署说明**
- 部署内容：复制EXE、写入配置文件、创建桌面快捷方式、设置托盘图标始终显示
- 部署时间：约3-8分钟（使用预制EXE，无需安装Python）
- 影响使用：部署过程静默完成，不影响电脑正常使用
- 涉及修改：修改注册表（托盘显示设置）

需用户回复同意后再开始部署。

**部署方式说明**：

**情况一：技能包内含预制EXE（推荐）**
- 条件：技能包ZIP内有 `ClipboardOCRV2.exe`（约35MB）
- 方式：直接复制EXE + 生成config.json + 创建快捷方式 + 设托盘不折叠
- 耗时：约3-8分钟
- 无需安装Python

**情况二：技能包内无EXE（EXE损坏/系统不兼容/需改快捷键）**
- 条件：技能包内无EXE或EXE无法运行
- 方式：从SKILL.md内嵌源码用PyInstaller打包，然后同情况一后续步骤
- 耗时：约3-8分钟
- 需Python环境 + pip install pyinstaller pystray pillow pyperclip requests pywin32

### 1. 部署EXE和配置文件

#### 1a. 检查EXE是否存在
```
检查路径: %USERPROFILE%\screenshot-ocr\ClipboardOCRV2.exe
```
如不存在，从技能包内复制预制EXE：
```bash
copy ClipboardOCRV2.exe %USERPROFILE%\screenshot-ocr\ClipboardOCRV2.exe
```

#### 1b. 检查config.json是否存在
```
检查路径: %USERPROFILE%\screenshot-ocr\config.json
```
如不存在，AI助手从 `~/.incaier-agent/sources/market-2bum-ocr/guide.md` 读取真实API地址和Access Key，写入：
```python
import json, os
# ⚠️ 强制规则：必须从guide.md读取真实值，不可使用占位符
cfg = {
    "api_url": "[从guide.md读取的API地址]",
    "api_key": "[从guide.md读取的X-Platform-Access-Key]"
}
with open(os.path.join(os.environ['USERPROFILE'], 'screenshot-ocr', 'config.json'), 'w', encoding='utf-8') as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
```
config.json格式：
```json
{
  "api_url": "https://market.haierfhtech.com/prod-api/capabilitymarket/api/v1/proxy/cap_beba5b924701433eb30790c66bb46f79",
  "api_key": "[用户的X-Platform-Access-Key]"
}
```

### 2. 检查快捷键是否被占用
默认快捷键为 `Ctrl+Shift+Z`。首次部署时需检测该快捷键是否被其他程序占用。

检测脚本：
```python
import ctypes, win32gui

MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004

hwnd = win32gui.CreateWindowEx(0, "static", "", 0, 0, 0, 0, 0, 0, 0, 0, None)
result = ctypes.windll.user32.RegisterHotKey(hwnd, 9999, MOD_CONTROL | MOD_SHIFT, ord('Z'))
if result:
    ctypes.windll.user32.UnregisterHotKey(hwnd, 9999)
    print("Ctrl+Shift+Z 可用")
else:
    print("Ctrl+Shift+Z 被占用，需更换")
win32gui.DestroyWindow(hwnd)
```

如被占用，备选快捷键：Ctrl+Shift+P、Ctrl+Shift+O。选定后修改源码中RegisterHotKey并重新打包。

### 3. 检查程序是否在运行
```bash
tasklist //FI "IMAGENAME eq ClipboardOCRV2.exe"
```
如未运行，启动：
```bash
start "" "%USERPROFILE%\screenshot-ocr\ClipboardOCRV2.exe"
```

### 4. 检查桌面快捷方式
```python
import os, win32com.client
shell = win32com.client.Dispatch('WScript.Shell')
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop', '截图OCR.lnk')
sc = shell.CreateShortcut(desktop)
sc.TargetPath = os.path.join(os.environ['USERPROFILE'], 'screenshot-ocr', 'ClipboardOCRV2.exe')
sc.WorkingDirectory = os.path.join(os.environ['USERPROFILE'], 'screenshot-ocr')
sc.Description = '截图OCR工具 - Ctrl+Shift+Z截屏+OCR'
sc.Save()
```

### 5. 设置托盘图标不折叠

按以下优先级依次尝试：

#### 方案一：直接运行现有脚本（最快）

检查 `%USERPROFILE%\screenshot-ocr\set_tray_visible.py` 是否存在：
```bash
python %USERPROFILE%\screenshot-ocr\set_tray_visible.py
```
- 成功：输出「已设置 IsPromoted=1」，托盘图标始终显示，结束
- 失败（文件不存在）：进入方案二
- 失败（未找到记录）：程序刚启动，Windows 尚未记录到注册表，等待5秒后重试，仍失败进入方案三

注意：脚本中TARGET_EXE需改为 `ClipboardOCRV2.exe`。

#### 方案二：现写脚本执行

AI 助手按以下源码写入 `%USERPROFILE%\screenshot-ocr\set_tray_visible.py` 后执行：

```python
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
```

写入后执行：
```bash
python %USERPROFILE%\screenshot-ocr\set_tray_visible.py
```

成功则结束，失败进入方案三。

#### 方案三：引导用户手动设置（保底）

请手动设置托盘图标始终显示：
1. 右键任务栏空白处 → 任务栏设置
2. 找到「其他系统托盘图标」
3. 找到 **ClipboardOCRV2**
4. 打开开关 → 开

或用命令直接打开设置页面：
```bash
start ms-settings:taskbar
```

### 6. 部署完成后
以上检查都通过后，**不需要重复执行**。部署完成后，先向用户告知部署路径：

**部署完成，文件位置如下：**
- 程序文件：`%USERPROFILE%\screenshot-ocr\ClipboardOCRV2.exe`
- 配置文件：`%USERPROFILE%\screenshot-ocr\config.json`
- 托盘脚本：`%USERPROFILE%\screenshot-ocr\set_tray_visible.py`
- 桌面快捷方式：`%USERPROFILE%\Desktop\截图OCR.lnk`

下次用户问起，直接发送以下内容给用户：

通过桌面"截图OCR"图标打开（桌面右下角托盘显示绿色小球表示已开启）
Ctrl+Shift+P 开关OCR（托盘图标绿色=开/灰色=关）
Ctrl+Shift+Z iHaier截图+OCR（模拟Ctrl+Shift+A）
Ctrl+Shift+X （模拟Win+Shift+S）
Ctrl+V粘贴识别出的文字
右键托盘→使用说明/开机自启/退出

## 源码

### clipboard_ocr_v2.py（v6.3 - 双快捷键+菜单说明+自启版）
```python
"""
剪贴板OCR工具 v6.3
- Ctrl+Shift+P = 开关OCR（绿=开/灰=关）
- Ctrl+Shift+Z = 模拟Ctrl+Shift+A截图+OCR（iHaier截图）
- Ctrl+Shift+X = 调用ms-screenclip:截图+OCR（Windows截图）
- 默认开启，右键菜单含使用说明、开机自启开关
"""

import time
import io
import sys
import os
import json
import struct
import subprocess
import threading
import tempfile
import requests
import pyperclip
from PIL import Image, ImageGrab, ImageDraw
import win32clipboard
import win32con
import win32gui
import winreg
import ctypes


def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "config.json")
    if not os.path.exists(config_path):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    if not os.path.exists(config_path):
        print("错误: 未找到config.json，请先配置API地址和密钥")
        os._exit(1)
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    return cfg.get("api_url", ""), cfg.get("api_key", "")

OCR_API_URL, OCR_API_KEY = load_config()

ocr_enabled = True
tray_icon = None
hotkey_hwnd = None
processing = False
autostart_enabled = False

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
WM_HOTKEY = 0x0312
HOTKEY_ID_P = 9001
HOTKEY_ID_Z = 9002
HOTKEY_ID_X = 9003

VK_LWIN = 0x5B
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_KEY_A = 0x41
VK_KEY_S = 0x53
VK_KEY_P = 0x50
VK_KEY_Z = 0x5A
VK_KEY_X = 0x58

AUTOSTART_REG_PATH = r'Software\Microsoft\Windows\CurrentVersion\Run'
AUTOSTART_REG_NAME = 'ClipboardOCRV2'
EXE_PATH = os.path.abspath(sys.argv[0]) if getattr(sys, 'frozen', False) else os.path.abspath(__file__)


def keybd_event(vk, flags=0):
    ctypes.windll.user32.keybd_event(vk, 0, flags, 0)


def simulate_ihaier_screenshot():
    keybd_event(VK_CONTROL, 0)
    keybd_event(VK_SHIFT, 0)
    keybd_event(VK_KEY_A, 0)
    time.sleep(0.05)
    keybd_event(VK_KEY_A, 2)
    keybd_event(VK_SHIFT, 2)
    keybd_event(VK_CONTROL, 2)


def simulate_windows_screenshot():
    subprocess.Popen('start ms-screenclip:', shell=True)


def get_clipboard_sequence():
    try:
        return win32clipboard.GetClipboardSequenceNumber()
    except Exception:
        return None


def clipboard_has_text():
    try:
        win32clipboard.OpenClipboard()
        try:
            has_text = (win32clipboard.IsClipboardFormatAvailable(13) or
                        win32clipboard.IsClipboardFormatAvailable(1) or
                        win32clipboard.IsClipboardFormatAvailable(15))
            return bool(has_text)
        finally:
            win32clipboard.CloseClipboard()
    except Exception:
        return False


def get_clipboard_image():
    try:
        img = ImageGrab.grabclipboard()
        if img is not None:
            if isinstance(img, Image.Image):
                return img
            if isinstance(img, list) and len(img) > 0:
                return Image.open(img[0])
    except Exception:
        pass
    try:
        win32clipboard.OpenClipboard()
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                if data:
                    bmp_header = b'BM'
                    file_size = len(data) + 14
                    bmp_header += struct.pack('<I', file_size)
                    bmp_header += b'\x00\x00\x00\x00'
                    bmp_header += struct.pack('<I', 14 + 40)
                    return Image.open(io.BytesIO(bmp_header + data))
        finally:
            win32clipboard.CloseClipboard()
    except Exception:
        pass
    return None


def ocr_image(image):
    try:
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)
        resp = requests.post(
            OCR_API_URL,
            headers={"X-Platform-Access-Key": OCR_API_KEY},
            files={"file": ("screenshot.png", buf, "image/png")},
            timeout=30
        )
        data = resp.json()
        if data.get("code") != 200:
            return None
        lines = []
        for page in data.get("result", {}).get("pages", []):
            for line in page.get("lines", []):
                text = line.get("text", "").strip()
                if text:
                    lines.append(text)
        return '\n'.join(lines)
    except Exception:
        return None


def make_icon_img(enabled):
    color = (0, 180, 0) if enabled else (160, 160, 160)
    img = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([6, 6, 58, 58], fill=color)
    draw.text((20, 18), "OCR", fill="white")
    return img


def check_autostart():
    global autostart_enabled
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, AUTOSTART_REG_PATH, 0, winreg.KEY_READ)
        try:
            val, _ = winreg.QueryValueEx(key, AUTOSTART_REG_NAME)
            autostart_enabled = True
        except FileNotFoundError:
            autostart_enabled = False
        winreg.CloseKey(key)
    except Exception:
        autostart_enabled = False
    return autostart_enabled


def set_autostart(enable):
    global autostart_enabled
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, AUTOSTART_REG_PATH, 0, winreg.KEY_SET_VALUE)
        if enable:
            winreg.SetValueEx(key, AUTOSTART_REG_NAME, 0, winreg.REG_SZ, f'"{EXE_PATH}"')
            autostart_enabled = True
        else:
            try:
                winreg.DeleteValue(key, AUTOSTART_REG_NAME)
            except FileNotFoundError:
                pass
            autostart_enabled = False
        winreg.CloseKey(key)
    except Exception as e:
        print(f"设置自启失败: {e}")
    update_tray_icon()


def toggle_autostart(icon, item):
    set_autostart(not autostart_enabled)


def show_help(icon, item):
    def show_msg():
        msg = (
            "快捷键：\n"
            "  Ctrl+Shift+P = 开关OCR（托盘图标绿色=开/灰色=关）\n"
            "  Ctrl+Shift+Z = iHaier截图+OCR（需iHaier开启）\n"
            "  Ctrl+Shift+X = Windows截图+OCR\n\n"
            "使用步骤：\n"
            "  1. 按Ctrl+Shift+Z或X截图\n"
            "  2. 框选屏幕区域\n"
            "  3. OCR自动识别，结果复制到剪贴板\n"
            "  4. Ctrl+V粘贴文字\n\n"
            "右键托盘图标可开关OCR、设置开机自启"
        )
        ctypes.windll.user32.MessageBoxW(0, msg, "截图OCR - 使用说明", 0x40)
    t = threading.Thread(target=show_msg, daemon=True)
    t.start()


def on_toggle(icon, item):
    toggle_ocr()


def on_quit(icon, item):
    icon.stop()
    os._exit(0)


def update_tray_icon():
    global tray_icon
    if tray_icon is None:
        return
    try:
        tray_icon.icon = make_icon_img(ocr_enabled)
        tray_icon.title = f"截图OCR - {'开启' if ocr_enabled else '关闭'}"
    except Exception:
        pass


def toggle_ocr():
    global ocr_enabled
    ocr_enabled = not ocr_enabled
    update_tray_icon()


def do_screenshot_ocr(use_ihaier):
    global processing
    if processing or not ocr_enabled:
        return
    processing = True
    seq_before = get_clipboard_sequence()
    if use_ihaier:
        simulate_ihaier_screenshot()
    else:
        simulate_windows_screenshot()
    for _ in range(100):
        time.sleep(0.1)
        seq_now = get_clipboard_sequence()
        if seq_now != seq_before:
            time.sleep(0.3)
            break
    else:
        processing = False
        return
    if clipboard_has_text():
        processing = False
        return
    img = get_clipboard_image()
    if img:
        text = ocr_image(img)
        if text and text.strip():
            pyperclip.copy(text)
        else:
            debug_path = os.path.join(tempfile.gettempdir(), "clipboard_ocr_debug.png")
            img.save(debug_path)
    processing = False


def hotkey_window_proc(hwnd, msg, wparam, lparam):
    if msg == WM_HOTKEY:
        if wparam == HOTKEY_ID_P:
            toggle_ocr()
        elif wparam == HOTKEY_ID_Z:
            t = threading.Thread(target=do_screenshot_ocr, args=(True,), daemon=True)
            t.start()
        elif wparam == HOTKEY_ID_X:
            t = threading.Thread(target=do_screenshot_ocr, args=(False,), daemon=True)
            t.start()
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)


def create_hotkey_window():
    global hotkey_hwnd
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = "ClipboardOCRHotkeyV2"
    wc.lpfnWndProc = hotkey_window_proc
    try:
        win32gui.RegisterClass(wc)
    except Exception:
        pass
    hotkey_hwnd = win32gui.CreateWindowEx(
        0, "ClipboardOCRHotkeyV2", "ClipboardOCRV2",
        0, 0, 0, 0, 0, 0, 0, 0, None
    )
    ctypes.windll.user32.RegisterHotKey(hotkey_hwnd, HOTKEY_ID_P, MOD_CONTROL | MOD_SHIFT, ord('P'))
    ctypes.windll.user32.RegisterHotKey(hotkey_hwnd, HOTKEY_ID_Z, MOD_CONTROL | MOD_SHIFT, ord('Z'))
    ctypes.windll.user32.RegisterHotKey(hotkey_hwnd, HOTKEY_ID_X, MOD_CONTROL | MOD_SHIFT, ord('X'))
    return hotkey_hwnd


def main():
    global tray_icon

    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    import socket
    try:
        single_lock_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        single_lock_sock.bind(('127.0.0.1', 47202))
        single_lock_sock.listen(1)
    except OSError:
        os._exit(0)

    check_autostart()
    create_hotkey_window()

    try:
        import pystray
        icon_img = make_icon_img(ocr_enabled)

        def get_ocr_label(icon=None, item=None):
            return f"OCR: {'✓开启' if ocr_enabled else '✗关闭'}"

        def get_autostart_label(icon=None, item=None):
            return f"开机自启: {'✓已开启' if autostart_enabled else '✗未开启'}"

        menu = pystray.Menu(
            pystray.MenuItem(get_ocr_label, on_toggle),
            pystray.MenuItem(get_autostart_label, toggle_autostart),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("使用说明", show_help),
            pystray.MenuItem("退出", on_quit),
        )

        tray_icon = pystray.Icon("ClipboardOCRV2", icon_img, f"截图OCR - {'开启' if ocr_enabled else '关闭'}", menu)

        def setup(icon):
            icon.visible = True
            def pump_messages():
                while True:
                    try:
                        win32gui.PumpWaitingMessages()
                    except Exception:
                        pass
                    time.sleep(0.01)
            t = threading.Thread(target=pump_messages, daemon=True)
            t.start()

        tray_icon.run(setup)

    except ImportError:
        while True:
            try:
                win32gui.PumpWaitingMessages()
            except Exception:
                pass
            time.sleep(0.05)


if __name__ == "__main__":
    main()

```

## 备选方案：从源码打包（当预制EXE不可用时）

适用场景：预制EXE无法运行（如系统不兼容）、需要修改快捷键、需要修改源码逻辑。

### 步骤
1. 将上方 clipboard_ocr_v2.py 源码写入 `%USERPROFILE%\screenshot-ocr\clipboard_ocr_v2.py`
2. 写入 config.json（同主方案1b）
3. 执行打包命令：
```bash
cd %USERPROFILE%\screenshot-ocr
python -m PyInstaller --onefile --name ClipboardOCRV2 --console --hidden-import=win32clipboard --hidden-import=win32gui --hidden-import=win32con --hidden-import=pystray --hidden-import=PIL.ImageDraw clipboard_ocr_v2.py
```
4. 复制EXE到目标目录：
```bash
copy dist\ClipboardOCRV2.exe %USERPROFILE%\screenshot-ocr\
```
5. 继续主方案的步骤2-5（快捷键检查、启动、快捷方式、托盘）

## 技能包文件清单

发布到技能市场时，ZIP包内应包含：
```
screenshot-ocr-v2.zip
├── SKILL.md              （技能说明+部署步骤+源码）
├── ClipboardOCRV2.exe    （预制EXE，不含密钥，约35MB）
└── set_tray_visible.py   （托盘不折叠脚本）
```

- ClipboardOCRV2.exe：预制版本，启动时从同目录config.json读取API配置，EXE本身不含任何密钥
- config.json：不打包在ZIP内，由AI助手在部署时从guide.md读取密钥后生成
- set_tray_visible.py：无敏感信息，直接打包（注意TARGET_EXE需改为ClipboardOCRV2.exe）

## 注意事项

- **仅限Windows平台**
- **必须用 --console 打包** + `ShowWindow(SW_HIDE)` 隐藏窗口（--noconsole下pystray不工作）
- **RegisterHotKey替代keyboard库**：--noconsole下keyboard库全局快捷键不生效，改用Windows原生RegisterHotKey API
- **Windows截图方式**：Ctrl+Shift+X调用ms-screenclip:协议直接打开Windows截图工具，不模拟Win键（Windows安全机制阻止模拟Win键）
- **无弹窗通知**：仅靠托盘图标颜色（绿色=开/灰色=关）指示状态
- **单实例锁**：通过本地socket绑定防止程序重复启动，仅本机通信，不涉及网络传输
- **OCR API**：使用能力市场 `market-2bum-ocr` 在线API（公共能力，所有用户自动可用，无需配置）。AI 助手部署时从 `~/.incaier-agent/sources/market-2bum-ocr/guide.md` 读取真实 Access Key，写入 `%USERPROFILE%\screenshot-ocr\config.json`，预制EXE启动时自动读取

## 踩坑经验（不要重走）

1. 自绘截图窗口全黑屏（10种GDI方案均失败）
2. --noconsole + keyboard库：快捷键不生效
3. --noconsole + pystray：托盘图标不显示
4. 最终方案：--console + ShowWindow(SW_HIDE) + RegisterHotKey + pystray
5. Ctrl+Shift+P被自身占用：ClipboardOCR自己注册了该键，检测时显示"被占用"是自身造成的
6. Windows截图：ms-screenclip:协议替代模拟Win+Shift+S（keybd_event无法模拟Win键，被Windows安全机制阻止）
