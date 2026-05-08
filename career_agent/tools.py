from retriever import search_jobs

def rewrite_query(user_input):

    keyword_map = {

        "เขียนโปรแกรม":
        "coding programming software developer python",

        "ทำอาหาร":
        "cooking chef culinary food restaurant",

        "วาดรูป":
        "design creative graphic art",

        "ช่วยคน":
        "healthcare counseling social work",

        "คิดเลข":
        "finance accounting analytics statistics"

    }

    expanded_query = user_input

    for key, value in keyword_map.items():

        if key in user_input:

            expanded_query += " " + value

    expanded_query += " career skills job"

    return expanded_query

def rank_jobs(jobs, scores):
    # WOW ⭐: ranking
    ranked = sorted(zip(jobs, scores), key=lambda x: x[1], reverse=True)
    return [j[0] for j in ranked]

def generate_roadmap(job):
    # WOW ⭐⭐
    return f"""
Career Path: {job['job_title']}

1. Learn basics of {job['skills']}
2. Build 2-3 projects
3. Create portfolio
4. Apply for internship/job
"""

def guardrail(scores):

    # ไม่มี retrieval result
    if len(scores) == 0:
        return False

    # score ต่ำเกิน
    if max(scores) < 0.45:
        return False

    return True