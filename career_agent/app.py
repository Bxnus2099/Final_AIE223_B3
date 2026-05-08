import streamlit as st
import pandas as pd
from agent import run_agent
from memory import get_memory

# Page Config
st.set_page_config(
    page_title="AI Career Coach Agent",
    page_icon="୨୧",
    layout="wide"
)

# INJECT PINK LACE PORTFOLIO THEME
def load_css(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css("style.css")

# Decorative lace + bow header ornament
st.markdown("""
<div class="portfolio-ornament top-ornament" aria-hidden="true">
    <span class="lace-line"></span>
    <span class="bow-mark">୨୧</span>
    <span class="lace-line"></span>
</div>
""", unsafe_allow_html=True)

# Title
st.title("AI Career Coach Agent")

st.markdown("""
### AI ที่ช่วยวิเคราะห์ความสนใจ, ความสามารถและแนะนำอาชีพที่เหมาะกับคุณ <3
""")

# Decorative lace footer ornament
st.markdown("""
<div class="portfolio-ornament bottom-ornament" aria-hidden="true">
    <span class="lace-line"></span>
    <span class="bow-mark small">✧</span>
    <span class="lace-line"></span>
</div>
""", unsafe_allow_html=True)

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

                import altair as alt

                chart = alt.Chart(score_df).mark_bar(
                 color="#ff8fd1"
                ).encode(
                 x=alt.X(
                        "Career",
                        sort=None
                 ),
                 y=alt.Y(
                      "Score"
                    )
                ).properties(
                    height=400
                )

                st.altair_chart(
                    chart,
                    use_container_width=True
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
