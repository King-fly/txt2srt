# txt2srt 📝→📼

简单高效的TXT转SRT字幕工具，支持带时间戳的TXT文件快速转换为标准SRT字幕格式。

## 特性
- ✅ 支持时间戳格式：`mm:ss`（分:秒）或 `hh:mm:ss`（时:分:秒）
- ✅ 自动处理文本分行（时间戳行后紧跟文本行）
- ✅ 支持自定义文件编码（默认 UTF-8）
- ✅ 命令行快速使用 + Python 库调用双模式
- ✅ 自动处理最后一条字幕的结束时间（默认延长3秒）

## 安装方法

### 方法1：本地源码安装（支持修改代码）
```bash
# 克隆仓库
git clone https://github.com/your-username/txt2srt.git
cd txt2srt

# 本地安装（支持 --editable 开发模式）
pip install .

# 开发模式（修改代码后无需重新安装）
pip install -e .