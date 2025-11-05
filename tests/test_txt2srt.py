"""txt2srt 测试用例"""
import tempfile
import os
from txt2srt import convert_txt_to_srt, txt_to_srt_content

def test_basic_conversion():
    """测试基本转换功能"""
    txt_content = """00:05
第一句字幕

00:10
第二句字幕

01:23:45
第三句字幕
"""
    
    # 临时文件测试
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as txt_file:
        txt_file.write(txt_content)
        txt_path = txt_file.name
    
    srt_path = tempfile.mktemp(suffix='.srt')
    
    try:
        convert_txt_to_srt(txt_path, srt_path)
        
        # 验证输出（修正预期结果，与实际转换逻辑一致）
        with open(srt_path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
        
        assert "1" in srt_content
        assert "00:00:05,000 --> 00:00:10,000" in srt_content  # 第一句结束时间=第二句开始时间
        assert "第一句字幕" in srt_content
        assert "00:00:10,000 --> 01:23:45,000" in srt_content  # 第二句结束时间=第三句开始时间
        assert "第二句字幕" in srt_content
        assert "01:23:45,000 --> 01:23:48,000" in srt_content  # 最后一句+3秒
        assert "第三句字幕" in srt_content
    finally:
        os.unlink(txt_path)
        os.unlink(srt_path)

def test_empty_text():
    """测试空文本字幕"""
    txt_lines = [
        "00:05",
        "",
        "00:10",
        "有文本的字幕"
    ]
    
    srt_content = txt_to_srt_content(txt_lines)
    assert "00:00:05,000 --> 00:00:10,000" in srt_content
    assert "\n\n2" in srt_content  # 空文本行（第一句字幕文本为空）
    assert "有文本的字幕" in srt_content

def test_time_format():
    """测试不同时间格式（有效/无效）"""
    txt_lines = [
        "123:45",  # 无效格式（3位数字，不匹配 \d{1,2}:\d{2}）
        "01:23:45",  # 有效（时:分:秒）
        "45:67",  # 无效（秒=67>59，但会被当作上一个有效时间戳的文本）
        "05:30",  # 有效（分:秒）
    ]
    
    srt_content = txt_to_srt_content(txt_lines)
    # 应该只解析到 2 个有效时间戳："01:23:45" 和 "05:30"
    assert srt_content.count("-->") == 2
    
    # 关键修正：第一句的结束时间是 01:23:48（+3秒），因为第二句的开始时间 00:05:30 早于第一句的开始时间 01:23:45
    # 程序会自动避免结束时间早于开始时间，所以第一句结束时间不会是第二句开始时间
    assert "01:23:45,000 --> 01:23:48,000" in srt_content  # 第一句：有效时间戳 + 下一行文本（45:67）
    assert "45:67" in srt_content  # 验证无效时间戳被当作上一句的文本
    assert "00:05:30,000 --> 00:05:33,000" in srt_content  # 第二句：有效时间戳，无后续文本

def test_invalid_time_value():
    """测试数值超出范围的时间戳"""
    txt_lines = [
        "00:60",  # 秒=60>59（无效，格式匹配但数值无效）
        "01:60:00",  # 分=60>59（无效，格式匹配但数值无效）
        "02:30",  # 有效
    ]
    
    srt_content = txt_to_srt_content(txt_lines)
    assert srt_content.count("-->") == 1  # 仅1个有效时间戳
    assert "00:02:30,000 --> 00:02:33,000" in srt_content