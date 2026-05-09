import pandas as pd

# ใช้ SentenceTransformer สำหรับสร้าง embedding vector
from sentence_transformers import SentenceTransformer
# ใช้ cosine similarity สำหรับวัดความใกล้เคียงของข้อความ
from sklearn.metrics.pairwise import cosine_similarity


# load Dataset

df = pd.read_csv("data/jobs.csv")


# โหลด Embedding Model
# ใช้ multilingual embedding model
# รองรับภาษาไทยและภาษาอังกฤษ
# ใช้แปลงข้อความเป็น vector embedding
model = SentenceTransformer(
    'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
)

# รวมข้อมูลแต่ละอาชีพ

# นำ job_title + skills + description
# มารวมเป็นข้อความเดียว
# เพื่อใช้สร้าง embedding
corpus = (
    df["job_title"] + " " +
    df["skills"] + " " +
    df["description"]
).tolist()

# สร้าง Embedding ของ Dataset
# แปลงข้อความทุกอาชีพ
# เป็น vector embedding
corpus_embeddings = model.encode(corpus)

# Semantic Search Function
def search_jobs(query, top_k=3):

    # แปลง Query เป็น Embedding
    # แปลงข้อความที่ user พิมพ์
    # เป็น vector embedding
    query_embedding = model.encode([query])

    # คำนวณ Similarity
    # เปรียบเทียบ query embedding
    # กับ embedding ของทุกอาชีพ
    # ด้วย cosine similarity
    sims = cosine_similarity(
        query_embedding,
        corpus_embeddings
    )[0]

    # กำหนด Threshold
    # dynamic threshold
    # ใช้ score สูงสุด * 0.8
    dynamic_threshold = max(sims) * 0.8

    # absolute threshold
    # กำหนดขั้นต่ำของ similarity
    absolute_threshold = 0.45

    # เลือก threshold ที่สูงกว่า
    threshold = max(
        dynamic_threshold,
        absolute_threshold
    )

    # เลือก Top Careers
    # เลือกเฉพาะอาชีพ
    # ที่ similarity มากกว่า threshold
    # และเลือก top_k อันดับแรก
    top_idx = [
        i for i in sims.argsort()[::-1]
        if sims[i] >= threshold
    ][:top_k]
 
    # สร้างผลลัพธ์
    results = []

    for idx in top_idx:

        # ดึงข้อมูลอาชีพจาก dataframe
        job = df.iloc[idx].to_dict()

        # เพิ่ม similarity score
        job["score"] = float(sims[idx])

        # เพิ่มเข้า results
        results.append(job)

    # Return Results

    # คืนค่า:รายชื่ออาชีพที่ใกล้เคียง และ similarity scores
    return results, sims[top_idx]