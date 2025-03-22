import openai

client = openai.OpenAI(api_key="enter_valid_API_key")

def ask_openai(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal advisor."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Testiranje
print(ask_openai("Objasni mi moja prava kao zaposlenog u Infinumu?"))
