import logging
import dashscope
from dashscope import Generation


API_KEY = "sk-d3e0c2eb1feb4b4aab36d1b770de8151"



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
    """调用通义千问 API 生成摘要"""
    logging.info("开始调用通义千问 API")
    dashscope.api_key = API_KEY

    messages = [
        {'role': 'system', 'content': '你是一个专业的文本摘要助手。'},
        {'role': 'user', 'content': f'请为以下文本生成一段简短的中文摘要（不超过100字）：\n\n{text}'}
    ]

    try:
        response = Generation.call(
            model='qwen-turbo',
            messages=messages,
            result_format='message'
        )
        if response.status_code == 200:
            summary = response.output.choices[0].message.content
            logging.info("API 调用成功")
            return summary
        else:
            error_msg = f"API 错误，状态码：{response.status_code}，信息：{response.message}"
            logging.error(error_msg)
            return error_msg
    except Exception as e:
        logging.error(f"调用异常: {e}")
        return f"调用失败: {e}"

def main():
    file_path = "sample.txt"
    print("程序启动，正在读取文件...")

    content = read_file(file_path)
    if content:
        print(f"文件读取成功，共 {len(content)} 字符")
        print("正在调用通义千问生成摘要...")
        summary = generate_summary(content)
        print("\n" + "="*50)
        print("生成的摘要：")
        print(summary)
        print("="*50)
    else:
        print("无法读取文件，程序结束")

if __name__ == "__main__":
    main()