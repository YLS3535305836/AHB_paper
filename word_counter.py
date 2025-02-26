import os
import re
import pdfplumber
from tqdm import tqdm


def count_chinese_chars(text):
    """统计中文字符数量（排除标点、空格和英文字母）"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')  # 仅匹配汉字
    return len(chinese_pattern.findall(text))


def is_valid_page(text):
    """判断是否为正文页：过滤目录、页眉、页脚等"""
    if not text or len(text) < 50:  # 过滤极短的页面（可能是页眉或页脚）
        return False
    if "目录" in text[:50] or "References" in text[:50]:  # 跳过目录页
        return False
    if re.search(r'^\s*第\s*\d+\s*页', text):  # 过滤掉页脚（"第 X 页"）
        return False
    return True


def count_pdf_words(pdf_path):
    """统计单个 PDF 文件正文部分的字数"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total = 0
            for page in pdf.pages:
                text = page.extract_text()
                if text and is_valid_page(text):
                    total += count_chinese_chars(text)
            return total
    except Exception as e:
        print(f"\n处理文件 {os.path.basename(pdf_path)} 时出错: {str(e)}")
        return 0


def batch_count_pdf_words(path):
    """统计路径（文件或文件夹）下 PDF 的正文字数"""
    if os.path.isfile(path):  # 单个文件
        words = count_pdf_words(path)
        print(f"文件统计完成: {os.path.basename(path)}")
        print(f"▋ 中文字符数: {words} 字")
        print(f"▋ 约合汉字数: {words} 字")
        print(f"▋ 约合英文字数: {words//6} 单词")

    elif os.path.isdir(path):  # 处理文件夹
        pdf_files = [f for f in os.listdir(path) if f.lower().endswith('.pdf')]
        total_words = 0

        print(f"开始扫描文件夹: {path}")
        print(f"找到 {len(pdf_files)} 个 PDF 文件")

        for filename in tqdm(pdf_files, desc="处理进度"):
            file_path = os.path.join(path, filename)
            words = count_pdf_words(file_path)
            total_words += words
            print(f"{filename}: {words} 字")  # 显示单个文件字数

        print(f"\n总字数统计完成")
        print(f"▋ 中文字符总数: {total_words} 字")
        print(f"▋ 约合汉字数: {total_words} 字（中文论文标准）")
        print(f"▋ 约合英文字数: {total_words//6} 单词（按 1:6 换算）")

    else:
        print(f"路径无效: {path} 既不是文件也不是目录")


if __name__ == "__main__":
    # target_path = r"D:/文档/陈瑶.pdf"
    target_path = r"D:/小米云盘/毕业相关/LATEX/tamako-paper/zwcpaper.pdf"
    batch_count_pdf_words(target_path)
