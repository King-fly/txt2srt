"""
txt2srt - 简单高效的TXT转SRT字幕工具
支持时间戳格式：mm:ss 或 hh:mm:ss
"""
from .core import (
    parse_time,
    td_to_srt,
    extract_time_text_pairs,
    txt_to_srt_content,
    convert_txt_to_srt
)
from .cli import main

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

__all__ = [
    "parse_time",
    "td_to_srt",
    "extract_time_text_pairs",
    "txt_to_srt_content",
    "convert_txt_to_srt",
    "main"
]