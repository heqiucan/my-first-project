import re
import dashscope
from dashscope import Generation
dashscope.api_key="sk-d3e0c2eb1feb4b4aab36d1b770de8151"
def load_document(file_path):
    """读取文本文件，返回内容"""
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            content=f.read()
        print(f"成功读取文件:{file_path}")
        return content
    except FileNotFoundError:
        print(f"错误:文件{file_path}不存在")
def split_paragraphs(text):
    """按俩个换行符切换段落，并去除空段落"""
    paragraphs=[p.strip() for p in text.split('\n\n') if p.strip()]
    print(f"共切分出{len(paragraphs)}个段落")
    return paragraphs
def extract_keywords(question):
    import re
    words=re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+',question)
    keywords=[w for w in words if len(w)>1]
    return keywords
def retrieve_paragraph(paragraphs,keywords):
    best_para=None
    best_score=-1
    for para in paragraphs:
        score =sum(para.count(kw) for kw in keywords)
        if score>best_score and score>0:
            best_score=score
            best_para=para
    return best_para,best_score
def ask_llm(question, context):
    if not context:
        return "未找到相关信息，无法回答。"
    prompt = f"根据以下内容回答问题：\n\n{context}\n\n问题：{question}\n\n答案："
    messages = [{'role': 'user', 'content': prompt}]
    try:
        response = Generation.call(
            model='qwen-turbo',
            messages=messages,
            result_format='message'
        )
        if response.status_code == 200:
            return response.output.choices[0].message.content
        else:
            return f"API错误: {response.message}"
    except Exception as e:
        return f"调用失败: {e}"

if __name__=='__main__':
     content=load_document("knowledge.txt")
     if content:
        paras=split_paragraphs(content)
        for i,p in enumerate(paras):
            print(f"段落{i+1}:{p[:50]}...")
     else:
         print("文件读取失败")

test_q="Python有哪些应用？"
kw=extract_keywords(test_q)
print("提起关键词:",kw)
best_para,score=retrieve_paragraph(paras,kw)
print(f"匹配的分:{score}")
if best_para:
    print(f"最佳段落:{best_para[:100]}...")
    answer=ask_llm(test_q,best_para)
    print("生成的答案:",answer)
else:
    print("未找到相关段落")

