import os
import requests
from groq import Groq
from dotenv import load_dotenv
from .prompts import node_connection_prompt
from .generate_architecture import generate_architecture_diagram
from . import llm_models

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def get_response_from_llm(prompt, system_prompt=node_connection_prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"{node_connection_prompt}"
                },
                {
                    "role": "user",
                    "content": f"{prompt}",
                }
            ],
            model=f"{llm_models.llama_70b_model}",
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        print(e)
        return ''



# CLOUD_SERVICE = "GCP"
# prompt = f"""
# can you help me in creation of architecture for deploying complex web application

# FOR CLOUD: {CLOUD_SERVICE}
# """
# output = get_response_from_llm(prompt)
# import json
# json_output = json.loads(output) or ''
# arch = json_output.get("architecture")
# breakpoint()
# ok = generate_architecture_diagram(arch)

