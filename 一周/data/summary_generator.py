import logging

# 配置日志（同时输出到控制台）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def read_file(file_path):
    """读取文本文件，返回内容，失败返回 None"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logging.info(f"成功读取文件: {file_path}")
        return content
    except FileNotFoundError:
        logging.error(f"文件不存在: {file_path}")
        print(f"错误：文件 {file_path} 未找到，请检查路径")
        return None
    except Exception as e:
        logging.error(f"读取文件出错: {e}")
        print(f"读取文件出错: {e}")
        return None


def generate_summary(text):
    """模拟生成摘要（不调用任何 API）"""
    logging.info("开始生成模拟摘要")

    # 基础统计
    char_count = len(text)
    word_count = len(text.split())
    line_count = text.count('\n') + 1

    # 简单摘要：取前 200 个字符作为摘要
    if len(text) > 200:
        summary_text = text[:200] + "..."
    else:
        summary_text = text

    # 你也可以改用“高频词”作为摘要（可选），这里保持简单
    result = (
        f"【文件统计】\n"
        f"字符数: {char_count}\n"
        f"单词数: {word_count}\n"
        f"行数: {line_count}\n\n"
        f"【模拟摘要】\n{summary_text}"
    )
    logging.info("模拟摘要生成完成")
    return result


def main():
    # 请确保 sample.txt 和本脚本在同一目录下，或修改为绝对路径
    file_path = "sample.txt"
    print("程序启动，正在读取文件...")

    content = read_file(file_path)
    if content:
        print(f"文件读取成功，共 {len(content)} 字符")
        print("\n正在生成摘要...\n")
        summary = generate_summary(content)
        print("=" * 50)
        print(summary)
        print("=" * 50)
    else:
        print("无法读取文件，程序结束")


if __name__ == "__main__":
    main()