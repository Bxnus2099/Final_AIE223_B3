# =========================
# Conversation Memory
# =========================

memory = {
    "history": []
}

# =========================
# Add Conversation
# =========================
def add_to_memory(user_input, response):

    memory["history"].append({
        "user": user_input,
        "assistant": response
    })

# =========================
# Get Full Memory
# =========================
def get_memory():

    return memory

# =========================
# Get Recent Context
# =========================
def get_recent_context(limit=1):

    history = memory["history"]

    recent = history[-limit:]

    context = ""

    for chat in recent:

        context += f"""
User: {chat['user']}
Assistant: {chat['assistant']}
"""

    return context