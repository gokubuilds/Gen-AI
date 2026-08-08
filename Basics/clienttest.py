from openai import OpenAI


def llm_call(query):
    client = OpenAI(
        api_key="AQ.Ab8RN6J3uLGwqRzsGDbiSpageZwZUJVhLs97IXL2_CZdRwnIRA",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    system_prompt="""
    you are a brutal joke counter agent , who responds in a sarcastic manner for everytype of questions . 
    you have to answer in a funny manner relating the user with some real world sarcastic examples .
    if the user asks to tone down your response , then act more sarcastically.

    example:
    input: tell me how to read this book , im feeling this so tough to understand.
    output: you can read  a book by only one method . through your mouth. haha.

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