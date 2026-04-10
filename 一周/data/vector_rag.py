import chromadb
import dashscope
import os
from dashscope import TextEmbedding, Generation

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
CHROMA_DATA_PATH = "./chroma_db"
DOCUMENT_PATH = "knowledge.txt"
EMBEDDING_MODEL = "text-embedding-v2"

def load_and_split_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def get_embeddings(texts):
    batch_size = 10
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        resp = TextEmbedding.call(model=EMBEDDING_MODEL, input=batch)
        if resp.status_code == 200:
            embeddings = [item['embedding'] for item in resp.output['embeddings']]
            all_embeddings.extend(embeddings)
        else:
            raise Exception(f"Embedding API 错误: {resp.message}")
    return all_embeddings

def get_or_create_collection():
    client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
    try:
        collection = client.get_collection(name="knowledge_base")
        print("使用已有集合")
    except ValueError:
        collection = client.create_collection(name="knowledge_base")
        print("创建新集合")
    return collection

def index_document(collection, paragraphs):
    if collection.count() > 0:
        print("数据库已有数据，跳过索引。如需重新索引，请删除目录", CHROMA_DATA_PATH)
        return
    print("正在生成段落向量...")
    embeddings = get_embeddings(paragraphs)
    ids = [f"para_{i}" for i in range(len(paragraphs))]
    collection.add(
        documents=paragraphs,
        embeddings=embeddings,
        ids=ids
    )
    print(f"已索引 {len(paragraphs)} 个段落")

def retrieve_paragraphs(collection, query, top_k=1):
    query_embedding = get_embeddings([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    if results['documents'] and results['documents'][0]:
        return results['documents'][0]
    else:
        return []

def ask_llm(question, context):
    if not context:
        return "未找到相关信息。"
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

if __name__ == "__main__":
    paragraphs = load_and_split_document(DOCUMENT_PATH)
    print(f"共 {len(paragraphs)} 个段落")
    if not paragraphs:
        print("文档为空或切分后无段落，请检查 knowledge.txt")
        exit()
    collection = get_or_create_collection()
    index_document(collection, paragraphs)
    query = "大语言模型的训练过程"
    results = retrieve_paragraphs(collection, query)
    print("检索结果:", results)
    if results:
        answer = ask_llm(query, results[0])
        print("答案:", answer)