import streamlit as st
from vector_rag import load_and_split_document, get_or_create_collection, index_document, retrieve_paragraphs, ask_llm

st.set_page_config(page_title="文档问答助手 (向量检索版)", page_icon="📚")
st.title("📚 文档问答助手 (向量检索版)")
st.markdown("基于 `knowledge.txt`，使用向量检索 + 通义千问")

@st.cache_resource
def init_vector_db():
    paragraphs = load_and_split_document("knowledge.txt")
    collection = get_or_create_collection()
    if collection.count() == 0:
        with st.spinner("正在建立向量索引（首次运行需要生成向量）..."):
            index_document(collection, paragraphs)
    return collection, paragraphs

collection, paragraphs = init_vector_db()
st.success(f"知识库已加载，共 {len(paragraphs)} 个段落，向量索引已就绪。")

question = st.text_input("请输入你的问题：")
if st.button("查询"):
    if not question:
        st.warning("请输入问题")
    else:
        with st.spinner("正在检索并生成答案..."):
            results = retrieve_paragraphs(collection, question, top_k=1)
            if results:
                answer = ask_llm(question, results[0])
                st.success("答案：")
                st.write(answer)
                with st.expander("查看相关段落"):
                    st.write(results[0])
            else:
                st.error("未找到相关段落，请尝试换个问法。")