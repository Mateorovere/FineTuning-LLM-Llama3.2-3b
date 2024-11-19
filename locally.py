import torch
from transformers import pipeline

model_id = "MateoRov/Llama3.2-3b-SFF-Infinity-MateoRovere"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    token = "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"
)
messages = [
    {"role": "system", "content": "You are an AI resercher, provide the most accurate responses to AI related questions!"},
    {"role": "user", "content": "What is a GAN?"},
]
outputs = pipe(
    messages,
    max_new_tokens=256,
)
print(outputs[0]["generated_text"][-1]['content'])