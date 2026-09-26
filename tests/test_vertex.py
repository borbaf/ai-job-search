import os
from google import genai

client = genai.Client(
    vertexai=True,
    project="coherent-voice-420518",
    location="us-central1",
)

resp = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="responda apenas OK",
)

print("SUCESSO - resposta do modelo:", resp.text)
