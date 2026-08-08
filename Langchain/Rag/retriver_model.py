from openai import OpenAI
def llm_call(query,pgcontent):
    client = OpenAI(
        api_key="YOUR-SAMPLE-API-KEY",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    system_prompt="""
  You are a pdf rag chatbot assistant . you answer relevantly based on the provided user query and page content.
  page content:{pgcontent}

    """
    response = client.chat.completions.create(
        model="gemini-3.6-flash",
        messages=[
            {   "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return(response.choices[0].message.content)
