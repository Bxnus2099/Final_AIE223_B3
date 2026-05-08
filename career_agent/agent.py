from tools import rewrite_query, rank_jobs, guardrail
from retriever import search_jobs

from memory import (
    add_to_memory,
    get_memory,
    get_recent_context
)

from llm import generate_llm_response


def run_agent(user_input):

    # =========================
    # 1. Rewrite Query
    # =========================
    query = rewrite_query(user_input)

    # =========================
    # 2. Memory Context
    # =========================
    memory_context = get_recent_context()

    # Add memory context into query
    if memory_context.strip() != "":
        query += " " + memory_context

    print("\n===== AGENT THINKING =====")
    print("Original Input:", user_input)
    print("Rewritten Query:", query)

    # =========================
    # 3. Retrieval
    # =========================
    jobs, scores = search_jobs(query)

    print("Retrieved Scores:", scores)

    # =========================
    # 4. Guardrail + Fallback
    # =========================
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

        response = generate_llm_response(fallback_prompt)

        # Save memory
        add_to_memory(user_input, response)

        logs = {
            "Original Input": user_input,
            "Rewritten Query": query,
            "Scores": [float(s) for s in scores],
            "Fallback Mode": True,
            "LLM Model": "llama3",
            "Memory Context": memory_context
        }

        return response, logs

    # =========================
    # 5. Ranking
    # =========================
    ranked_jobs = rank_jobs(jobs, scores)

    # =========================
    # 6. Memory Data
    # =========================
    memory_data = get_memory()

    # =========================
    # 7. Confidence
    # =========================
    confidence = max(scores)

    # =========================
    # 8. Personality Analysis
    # =========================
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

    personality = generate_llm_response(personality_prompt)

    # =========================
    # 9. Dynamic Roadmap
    # =========================
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

    roadmap = generate_llm_response(roadmap_prompt)

    # =========================
    # 10. Main Prompt
    # =========================
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

    # =========================
    # 11. LLM Generation
    # =========================
    response = generate_llm_response(prompt)

    # =========================
    # 12. Matching Scores
    # =========================
    response += "\n\n📊 Matching Scores:\n"

    for job, score in zip(ranked_jobs, scores):

        response += (
            f"- {job['job_title']} : {score:.2f}\n"
        )

    # =========================
    # 13. Save Conversation Memory
    # =========================
    add_to_memory(user_input, response)

    # =========================
    # 14. Logs
    # =========================
    logs = {
        "Original Input": user_input,
        "Rewritten Query": query,
        "Scores": [float(s) for s in scores],
        "Top Career": ranked_jobs[0]["job_title"],
        "Confidence": float(confidence),
        "Fallback Mode": False,
        "LLM Model": "llama3",
        "Retrieved Careers": [
            job["job_title"] for job in ranked_jobs
        ],
        "Memory Context": memory_context
    }

    return response, logs