"""txt2srt - 转换带时间戳的TXT文件为SRT字幕文件"""
from datetime import timedelta
import re
from typing import List, Tuple

def parse_time(time_str: str) -> timedelta:
    """
    解析时间字符串为timedelta对象
    支持格式：mm:ss 或 hh:mm:ss
    """
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 2:
        m, s = parts
        if s >= 60:  # 新增：秒数不能超过59
            raise ValueError(f"秒数超出范围（0-59）: {s}")
        return timedelta(minutes=m, seconds=s)
    elif len(parts) == 3:
        h, m, s = parts
        if m >= 60 or s >= 60:  # 新增：分钟和秒数不能超过59
            raise ValueError(f"分钟或秒数超出范围（0-59）: {m}:{s}")
        return timedelta(hours=h, minutes=m, seconds=s)
    else:
        raise ValueError(f"无效的时间格式: {time_str}（支持 mm:ss 或 hh:mm:ss）")

def td_to_srt(td: timedelta) -> str:
    """
    将timedelta对象转换为SRT格式的时间字符串（hh:mm:ss,mmm）
    """
    secs = int(td.total_seconds())
    ms = td.microseconds // 1000
    h = secs // 3600
    m = (secs % 3600) // 60
    s = secs % 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def extract_time_text_pairs(lines: List[str]) -> List[Tuple[str, str]]:
    """
    从TXT文件行中提取（时间戳字符串，文本）对
    修复：无效时间戳后不读取文本，避免误解析
    """
    pairs = []
    i = 0
    time_pattern = re.compile(r'^\d{1,2}:\d{2}(?::\d{2})?$')  # 仅匹配格式，不验证数值范围
    
    while i < len(lines):
        line = lines[i].strip()
        if time_pattern.match(line):
            # 先尝试解析时间戳（验证数值范围）
            try:
                parse_time(line)  # 仅用于验证，实际转换时会再调用
                time_str = line
            except ValueError:
                # 无效时间戳，跳过当前行
                i += 1
                continue
            
            # 读取下一行作为文本（支持空文本）
            text = lines[i + 1].strip() if (i + 1 < len(lines)) else ""
            pairs.append((time_str, text))
            i += 2  # 跳过时间行和文本行
        else:
            i += 1  # 不是时间格式，继续下一行
    
    if not pairs:
        raise ValueError("未找到任何有效的时间戳（格式：mm:ss 或 hh:mm:ss，数值范围：分/秒 ≤59）")
    
    return pairs

def txt_to_srt_content(txt_lines: List[str]) -> str:
    """
    将TXT文件内容（行列表）转换为SRT格式字符串
    """
    pairs = extract_time_text_pairs(txt_lines)
    srt_lines = []
    
    for idx, (start_str, text) in enumerate(pairs, 1):
        start_td = parse_time(start_str)
        # 确定结束时间：下一个时间戳或当前时间+3秒
        if idx < len(pairs):
            end_td = parse_time(pairs[idx][0])
        else:
            end_td = start_td + timedelta(seconds=3)
        
        # 避免结束时间早于开始时间
        if end_td <= start_td:
            end_td = start_td + timedelta(seconds=3)
        
        srt_lines.extend([
            str(idx),
            f"{td_to_srt(start_td)} --> {td_to_srt(end_td)}",
            text,
            ""  # 字幕块之间的空行
        ])
    
    return '\n'.join(srt_lines).rstrip('\n')  # 移除末尾多余空行

def convert_txt_to_srt(txt_file: str, srt_file: str, encoding: str = 'utf-8') -> None:
    """
    主函数：读取TXT文件，转换为SRT文件并保存
    """
    # 读取TXT文件
    with open(txt_file, 'r', encoding=encoding) as f:
        txt_lines = [line.rstrip('\n') for line in f]
    
    # 转换为SRT内容
    srt_content = txt_to_srt_content(txt_lines)
    
    # 保存SRT文件
    with open(srt_file, 'w', encoding=encoding) as f:
        f.write(srt_content)