# import tools 
# จากไฟล์ tools.py
from tools import rewrite_query, rank_jobs, guardrail

# import semantic retrieval function
# จาก retriever.py
from retriever import search_jobs

# import memory functions
# จาก memory.py
from memory import (
    add_to_memory,
    get_memory,
    get_recent_context
)

# import function สำหรับเรียก LLM
# จาก llm.py
from llm import generate_llm_response

# Main Agent Function

def run_agent(user_input):
    # 1. Rewrite Query
    # ปรับ query ของ user
    # เพื่อเพิ่ม keyword และ context
    query = rewrite_query(user_input)


    # 2. Memory Context
    # ดึง conversation ล่าสุด
    # จาก memory system
    memory_context = get_recent_context()

    # ถ้ามี memory context
    # ให้นำมาต่อท้าย query
    # เพื่อช่วย retrieval
    if memory_context.strip() != "":
        query += " " + memory_context


    # Debug Logs
    print("\n===== AGENT THINKING =====")
    print("Original Input:", user_input)
    print("Rewritten Query:", query)


    # 3. Retrieval
    # ค้นหา careers
    # ด้วย semantic search
    jobs, scores = search_jobs(query)

    print("Retrieved Scores:", scores)


    # 4. Guardrail + Fallback
    # ถ้า retrieval quality ต่ำ
    # ให้เข้า fallback mode
    if not guardrail(scores):

        fallback_prompt = f"""

You are an intelligent AI Career Coach.

The retrieval system could not find strong matches.

Conversation History:
{memory_context}

User Interest:
{user_input}

Please:
- Suggest careers based on reasoning
- Explain why they fit
- Give career advice
- Answer in Thai
- Be friendly and helpful

"""

        # generate response จาก LLM
        response = generate_llm_response(
            fallback_prompt
        )

        # save conversation ลง memory
        add_to_memory(
            user_input,
            response
        )

        # สร้าง logs
        logs = {

            "Original Input":
            user_input,

            "Rewritten Query":
            query,

            "Scores":
            [float(s) for s in scores],

            "Fallback Mode":
            True,

            "LLM Model":
            "llama3",

            "Memory Context":
            memory_context
        }

        # return fallback response
        return response, logs

    # 5. Ranking
    # sort careers ตาม similarity score
    ranked_jobs = rank_jobs(
        jobs,
        scores
    )


    # 6. Memory Data
    # ดึง memory ทั้งหมด
    memory_data = get_memory()

    # 7. Confidence

    # ใช้ similarity score สูงสุด
    # เป็น confidence score
    confidence = max(scores)


    # 8. Personality Analysis
    # prompt สำหรับวิเคราะห์ personality
    personality_prompt = f"""

Analyze the user's personality traits and strengths.

Conversation History:
{memory_context}

User Input:
{user_input}

Return:
- Personality Traits
- Strengths
- Weaknesses
- Best Working Style

Do NOT use MBTI types.

Answer in Thai.

"""
    
    # generate personality analysis
    personality = generate_llm_response(
        personality_prompt
    )


    # 9. Dynamic Roadmap
    # prompt สำหรับสร้าง roadmap
    roadmap_prompt = f"""

Create a career roadmap for this user.

Career:
{ranked_jobs[0]["job_title"]}

User Interest:
{user_input}

Conversation History:
{memory_context}

Create:
- Beginner Steps
- Intermediate Skills
- Advanced Career Path

Answer in Thai.

"""

    # generate roadmap
    roadmap = generate_llm_response(
        roadmap_prompt
    )



    # 10. Main Prompt
    # prompt หลักสำหรับ career recommendation
    prompt = f"""

You are an intelligent AI Career Coach.

Conversation History:
{memory_context}

User Interest:
{user_input}

Retrieved Careers:
{ranked_jobs}

Memory:
{memory_data}

Confidence Score:
{confidence}

Personality Analysis:
{personality}

Career Roadmap:
{roadmap}

Instructions:
- Recommend careers that best match the user
- ONLY recommend careers from Retrieved Careers
- DO NOT invent careers outside retrieved results
- Prioritize retrieval results over assumptions
- Explain WHY they match
- Mention strengths and personality traits
- Explain career opportunities
- Give career advice
- Be realistic and grounded
- Answer in Thai
- Be friendly and professional
- Recommend ONLY careers with high similarity scores
- Ignore careers with weak relevance
- If careers are unrelated, say retrieval quality is low

"""


    # 11. LLM Generation
    # generate final response จาก LLM
    response = generate_llm_response(
        prompt
    )


    # 12. Matching Scores
    # เพิ่ม similarity scores
    # ลงใน response
    response += "\n\n📊 Matching Scores:\n"

    for job, score in zip(
        ranked_jobs,
        scores
    ):

        response += (
            f"- {job['job_title']} : {score:.2f}\n"
        )


    # 13. Save Conversation Memory
    # save conversation ลง memory
    add_to_memory(
        user_input,
        response
    )

    # 14. Logs
    # สร้าง logs
    # สำหรับ debug และ UI
    logs = {

        "Original Input":
        user_input,

        "Rewritten Query":
        query,

        "Scores":
        [float(s) for s in scores],

        "Top Career":
        ranked_jobs[0]["job_title"],

        "Confidence":
        float(confidence),

        "Fallback Mode":
        False,

        "LLM Model":
        "llama3",

        "Retrieved Careers":
        [
            job["job_title"]
            for job in ranked_jobs
        ],

        "Memory Context":
        memory_context
    }

    # return final response และ logs
    return response, logs