# =========================
# Conversation Memory
# =========================

# สร้าง dictionary สำหรับเก็บ memory
# โดยเก็บประวัติการสนทนาไว้ใน history
memory = {
    "history": []
}


# =========================
# Add Conversation
# =========================

def add_to_memory(user_input, response):

    # เพิ่มข้อมูลบทสนทนาใหม่เข้า memory
    # โดยเก็บ:
    # - ข้อความของ user
    # - ข้อความตอบของ assistant
    memory["history"].append({

        "user": user_input,

        "assistant": response
    })


# =========================
# Get Full Memory
# =========================

def get_memory():

    # return memory ทั้งหมด
    # สำหรับใช้แสดงใน UI หรือ debug
    return memory


# =========================
# Get Recent Context
# =========================

def get_recent_context(limit=1):

    # ดึง history ทั้งหมดจาก memory
    history = memory["history"]

    # เลือกเฉพาะบทสนทนาล่าสุด
    # ตามจำนวน limit
    recent = history[-limit:]

    # สร้าง context string
    context = ""

    # loop รวมบทสนทนา
    for chat in recent:

        # format conversation
        # ให้อยู่ในรูปแบบ:
        # User:
        # Assistant:
        context += f"""
User: {chat['user']}
Assistant: {chat['assistant']}
"""

    # return recent conversation context
    # เพื่อใช้เป็น context ให้ LLM
    return context