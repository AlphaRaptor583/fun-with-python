from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
