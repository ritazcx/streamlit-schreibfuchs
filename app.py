import streamlit as st
import os
import requests
from dotenv import load_dotenv
from utils import extract_scores, parse_file, build_prompt

# Load API key
load_dotenv()
# api_key = os.getenv("DEEPSEEK_API_KEY")
api_key = st.secrets["DEEPSEEK_API_KEY"]

API_URL = "https://api.deepseek.com/v1/chat/completions"

# Streamlit UI
st.set_page_config(page_title="SchreibFuchs", layout="wide")
st.title("🦊 SchreibFuchs - DeepSeek德语作文修改器")

st.header("📁 上传你的德语作文文件或直接粘贴文本")
uploaded_file = st.file_uploader("支持 .txt, .pdf, .docx", type=["txt", "pdf", "docx"])
essay_text = ""

if uploaded_file:
    essay_text = parse_file(uploaded_file)
    st.success("文件已成功解析！")
else:
    essay_text = st.text_area("或者粘贴你的德语作文", height=250)

style = st.radio("选择风格", ["Academic", "Casual", "Business"])
aim = st.radio("选择目标", ["Improve exam score", "Natural expression", "Enhance structure"])

if st.button("→ 修改我的作文"):
    if not essay_text.strip():
        st.warning("请先上传文件或输入文本！")
    else:
        with st.spinner("🦊 正在等待 DeepSeek 响应，请稍候..."):
            prompt = build_prompt(essay_text, style, aim)

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "top_p": 0.95,
                "max_tokens": 3000
            }

            try:
                response = requests.post(API_URL, headers=headers, json=data, timeout=120)
                result = response.json()

                if "choices" in result and result["choices"]:
                    output = result["choices"][0]["message"]["content"]
                    st.success("修改完成！")
                    st.header("🛠️ 修改建议与改写结果")
                    st.markdown(output)

                    # 📊 Show scoring chart
                    scores = extract_scores(output)
                    if scores:
                        # st.subheader("📊 评分图表")
                        st.bar_chart(scores)
                        for label, score in scores.items():
                            st.metric(label=label, value=f"{score}/5")
                    else:
                        st.info("未能识别评分数据，请检查模型返回内容。")

                    st.download_button("📥 下载结果", output, file_name="SchreibFuchs_Essay.txt")
                else:
                    st.error("API 没有返回有效结果，请检查输入或稍后再试。")

            except Exception as e:
                st.error(f"出错了：{e}")

