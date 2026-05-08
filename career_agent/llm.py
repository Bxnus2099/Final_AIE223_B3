# import ollama library
# สำหรับเรียกใช้งาน local LLM
import ollama

# Generate LLM Response
def generate_llm_response(prompt):

    # ส่ง prompt ไปยัง LLM model
    # ผ่าน ollama.chat()
    response = ollama.chat(

        # ใช้ model llama3
        model='llama3',

        # ส่งข้อความเข้า model
        messages=[
            {

                # role ของข้อความ
                # ในที่นี้คือ user prompt
                'role': 'user',

                # เนื้อหาของ prompt
                'content': prompt
            }
        ]
    )

    # return ข้อความตอบกลับจาก LLM
    return response['message']['content']