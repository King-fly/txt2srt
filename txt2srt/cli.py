"""txt2srt 命令行工具"""
import sys
import argparse
from txt2srt.core import convert_txt_to_srt

def main():
    parser = argparse.ArgumentParser(
        description="将带时间戳的TXT文件转换为SRT字幕文件",
        epilog="示例：txt2srt input.txt output.srt --encoding utf-8"
    )
    
    # 必选参数
    parser.add_argument(
        "input",
        help="输入TXT文件路径（时间戳格式：mm:ss 或 hh:mm:ss）"
    )
    parser.add_argument(
        "output",
        help="输出SRT文件路径"
    )
    
    # 可选参数
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="文件编码（默认：utf-8）"
    )
    
    args = parser.parse_args()
    
    try:
        convert_txt_to_srt(args.input, args.output, args.encoding)
        print(f"✅ 转换成功！SRT文件已保存至：{args.output}")
    except Exception as e:
        print(f"❌ 转换失败：{str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()