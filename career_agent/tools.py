# import function search_jobs
# จากไฟล์ retriever.py
from retriever import search_jobs

# Query Rewrite Function
def rewrite_query(user_input):

    keyword_map = {

    # dictionary สำหรับ map keyword
    # เพื่อช่วยขยาย query
        # ถ้า user สนใจเขียนโปรแกรม
        # เพิ่ม keyword เกี่ยวกับ software

        "เขียนโปรแกรม":
        "coding programming software developer python",

        # ถ้า user สนใจทำอาหาร
        # เพิ่ม keyword ด้าน culinary
        "ทำอาหาร":
        "cooking chef culinary food restaurant",

        # ถ้า user สนใจวาดรูป
        # เพิ่ม keyword ด้าน graphic art
        "วาดรูป":
        "design creative graphic art",

        # ถ้า user ช่วยคน
        # เพิ่ม keyword ด้าน healthcare
        "ช่วยคน":
        "healthcare counseling social work",

        # ถ้า user ชอบคำนวณ
        # เพิ่ม keyword ด้าน finance และ analytics
        "คิดเลข":
        "finance accounting analytics statistics"

    }

   # เริ่มต้น query ด้วยข้อความที่ user พิมพ์
    expanded_query = user_input

    # loop ตรวจสอบ keyword
    for key, value in keyword_map.items():

        # ถ้าพบ keyword ในข้อความ user
        if key in user_input:

            # เพิ่ม keyword expansion เข้า query
            expanded_query += " " + value

    # เพิ่ม context ทั่วไปเกี่ยวกับ career
    expanded_query += " career skills job"

    # return query ที่ rewrite แล้ว
    return expanded_query


# Ranking Function
def rank_jobs(jobs, scores):

    # zip jobs กับ scores เข้าด้วยกัน
    # แล้ว sort ตาม score จากมากไปน้อย
    ranked = sorted(zip(jobs, scores), key=lambda x: x[1], reverse=True)

    # return เฉพาะ job
    return [j[0] for j in ranked]


# Generate Career Roadmap
def generate_roadmap(job):

    # สร้าง roadmap พื้นฐาน
    # สำหรับ career ที่แนะนำ
    return f"""
Career Path: {job['job_title']}

1. Learn basics of {job['skills']}
2. Build 2-3 projects
3. Create portfolio
4. Apply for internship/job
"""

# Guardrail Function
def guardrail(scores):

    # ถ้าไม่มี retrieval result
    # return False
    if len(scores) == 0:
        return False

    # ถ้า similarity score ต่ำเกิน threshold
    # ถือว่า retrieval quality ไม่ดี
    if max(scores) < 0.45:
        return False

    # ถ้า retrieval ผ่านเงื่อนไข
    # return True
    return True