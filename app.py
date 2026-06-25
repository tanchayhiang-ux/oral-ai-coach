import streamlit as st
import pandas as pd
from openai import OpenAI
from oral_bank import get_topic
from scoring import get_badge
import os

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

st.set_page_config(
    page_title="华文口试AI教练",
    layout="wide"
)

st.title("🎤 华文口试AI教练")

# ------------------
# Student Details
# ------------------

name = st.text_input("学生姓名")

student_class = st.text_input("班级")

# ------------------
# Topic
# ------------------

if "topic" not in st.session_state:
    st.session_state.topic = get_topic()

topic = st.session_state.topic

st.image(topic["picture"], width=700)

st.subheader("口试题目")

st.write(topic["question"])

# ------------------
# Student Response
# ------------------

answer = st.text_area(
    "请输入你的回答",
    height=200
)

# ------------------
# AI Scoring
# ------------------

if st.button("提交评分"):

    if answer == "":
        st.warning("请输入回答")
        st.stop()

    prompt = f"""
你是一位经验丰富的新加坡小学华文老师。

学生年龄10岁。

题目：
{topic['question']}

学生回答：
{answer}

请评分：

内容10分
表达10分
词汇5分
语音5分

输出：

总分：
内容：
表达：
词汇：
语音：

优点：

建议：

示范答案：
"""

    result = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    feedback = result.choices[0].message.content

    st.success("评分完成")

    st.markdown(feedback)

    score = 20

    badge = get_badge(score)

    st.metric("获得徽章", badge)

    # Save Results

    row = pd.DataFrame([{
        "Name":name,
        "Class":student_class,
        "Topic":topic["question"],
        "Score":score
    }])

    if os.path.exists("student_results.csv"):

        old = pd.read_csv("student_results.csv")

        df = pd.concat([old,row])

    else:

        df = row

    df.to_csv(
        "student_results.csv",
        index=False
    )

# ------------------
# Teacher Dashboard
# ------------------

st.divider()

st.header("教师仪表板")

if os.path.exists("student_results.csv"):

    data = pd.read_csv(
        "student_results.csv"
    )

    st.dataframe(data)

    st.download_button(
        "下载Excel",
        data.to_csv(index=False),
        file_name="oral_results.csv"
    )

# ------------------
# Next Topic
# ------------------

if st.button("下一题"):

    st.session_state.topic = get_topic()
    st.rerun()
