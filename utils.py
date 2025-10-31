import re

# Extract scores from DeepSeek response
def extract_scores(text):
    pattern = r"(Sprache|Inhalt|Struktur):\s*(\d)/5"
    matches = re.findall(pattern, text)
    scores = {label: int(score) for label, score in matches}
    return scores

# Parse uploaded file into plain text
def parse_file(uploaded_file):
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    elif uploaded_file.name.endswith(".pdf"):
        import fitz  # PyMuPDF
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    elif uploaded_file.name.endswith(".docx"):
        from docx import Document
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        return "⚠️ 不支持的文件类型，请上传 .txt, .pdf 或 .docx 文件。"

# Optional: Build prompt from user input
def build_prompt(essay, style, aim):
    return f"""
你是一位专业的德语写作教练。请根据以下德语作文，提供以下内容：
1. 修改建议：列出语法错误、表达不自然、重复词汇、结构问题，并说明如何改进。
2. 改写后的版本：请用更自然、准确的德语表达，风格为 {style}，目标为 {aim}。
3. 简要评分预测：请使用以下格式：Sprache: x/5, Inhalt: x/5, Struktur: x/5，并说明理由。

德语作文如下：
{essay}
"""

