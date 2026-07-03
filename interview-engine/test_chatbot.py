from app.chatbot import chat_response

# Turn 1 — start the interview
history = []
user_message = "I'm ready to start. I'm applying for a Python backend developer role."

result = chat_response(history, user_message)
print("Interviewer:", result["reply"])
print()

# Turn 2 — answer the question properly
history = [
    {"role": "user", "content": user_message},
    {"role": "model", "content": result["reply"]}
]
user_message_2 = "A list is mutable so you can change its contents after creation, while a tuple is immutable. Lists use square brackets and tuples use parentheses. Tuples are faster and used for fixed data like coordinates."

result2 = chat_response(history, user_message_2)
print("Interviewer:", result2["reply"])
print()

# Turn 3 — continue
history.append({"role": "user", "content": user_message_2})
history.append({"role": "model", "content": result2["reply"]})
user_message_3 = "I would use a tuple for things like RGB colour values or database row records that shouldn't change."

result3 = chat_response(history, user_message_3)
print("Interviewer:", result3["reply"])