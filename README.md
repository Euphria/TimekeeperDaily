# Timekeeper Daily

用于自动启动游戏，并通过全屏图像匹配完成登录流程。

- [x] 启动1999客户端
- [x] 成功login
- [ ] 能完美进入homepage（由于login之后进入homepage过程中可能有多种奖励领取界面不好处理，所以这边统一等待用户手动操作结束进入homepage之后，再进行接下来的流程）
- [x] 能退出
- [x] 建立从homepage进入 **入场** 的操作链
- [x] 建立从 **入场** 到 **资源** 的操作链
- [x] 建立从 **资源** 到 **铸币**，**尘埃**，**意志** 的操作链
- [x] 建立完善战斗接口（进入，等待，退出到homepage）
- [x] 建立领取任务奖励接口（日活，周活）
- [ ] homepage点角色加好感
- [ ] 建立 **点唱机** 
- [ ] 任务及奖励领取接口
- [ ] 添加 **不休荒原** 操作链

## 环境

本地环境：

- Windows 11
- Python 3.10

安装依赖：

```powershell
python -m pip install --upgrade pip
pip install pywin32 mss opencv-python numpy pydirectinput pyyaml
```

## 运行

```powershell
python main.py
```

## 目标图片

目标图片放在 `targets` 目录中：

- `start.png`: 开始游戏按钮
- `home_page.png`: 游戏主页画面

当前识别逻辑会直接截取全屏，并按照目标图片的原始尺寸从截图左上角开始滑动匹配。目标图尺寸应尽量来自同一屏幕缩放比例下的截图。
