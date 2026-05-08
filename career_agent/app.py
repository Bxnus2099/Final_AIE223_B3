import streamlit as st
import pandas as pd

from agent import run_agent
from memory import get_memory

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="AI Career Coach Agent",
    page_icon="💼",
    layout="wide"
)

# Title
st.title("💼 AI Career Coach Agent")

st.markdown("""
### AI ที่ช่วยวิเคราะห์ความสนใจ, ความสามารถและแนะนำอาชีพที่เหมาะกับคุณ <3
""")

st.divider()

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🧠 AI Model", "Llama3")

with col2:
    st.metric("📂 Careers", "20+")

with col3:
    st.metric("⚡ Agent Status", "Running")


# User Input
user_input = st.text_area(
    "🧠 คุณสนใจอะไร หรือมี skill อะไร?",
    placeholder="เช่น ชอบวิเคราะห์ข้อมูล เขียนโปรแกรม ออกแบบ ทำอาหาร ฯลฯ",
    height=150
)


# Analyze Button
if st.button("🔍 วิเคราะห์อาชีพ", use_container_width=True):

    if user_input.strip() == "":

        st.warning("⚠ กรุณากรอกข้อมูลก่อน")

    else:

        # Spinner
        with st.spinner("🤖 AI Agent กำลังวิเคราะห์..."):

            result, logs = run_agent(user_input)

        st.success("✅ วิเคราะห์เสร็จแล้ว!")

        st.divider()

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Recommendation",
            "📊 Scores",
            "📜 Agent Logs",
            "🧠 Memory"
        ])


        # Recommendation Tab
        with tab1:

            st.subheader("🎯 Career Recommendation")

            st.write(result)

        # Score Visualization
        with tab2:

            st.subheader("📊 Matching Scores")

            if (
                "Scores" in logs and
                "Retrieved Careers" in logs
            ):

                score_df = pd.DataFrame({
                    "Career": logs["Retrieved Careers"],
                    "Score": logs["Scores"]
                })

                st.bar_chart(
                    score_df.set_index("Career")
                )

            else:

                st.warning("ไม่มีข้อมูล score")

            st.info(
                "คะแนนแสดงความใกล้เคียงระหว่าง user query กับ career dataset"
            )

  
        # Logs
        with tab3:

            st.subheader("📜 Agent Logs")

            st.json(logs)

            st.divider()

            st.subheader("🧠 Agent Workflow")

            st.write("1️⃣ Query Rewrite")
            st.write("2️⃣ Query Expansion")
            st.write("3️⃣ Semantic Retrieval")
            st.write("4️⃣ Guardrail Checking")
            st.write("5️⃣ Personality Analysis")
            st.write("6️⃣ Career Ranking")
            st.write("7️⃣ Dynamic Roadmap")
            st.write("8️⃣ LLM Reasoning")
            st.write("9️⃣ Memory Augmentation")

      
        # Memory
        with tab4:

            st.subheader("🧠 Conversation Memory")

            memory_data = get_memory()

            if memory_data:

                st.json(memory_data)

            else:

                st.info("ยังไม่มีข้อมูล memory")

# Dataset Viewer

st.divider()

with st.expander("📂 View Career Dataset"):

    df = pd.read_csv("data/jobs.csv")

    st.dataframe(
        df,
        use_container_width=True
    )