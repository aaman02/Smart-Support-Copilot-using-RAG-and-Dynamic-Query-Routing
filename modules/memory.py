def get_chat_history(chat_history):

    return "\n".join(
        [f"{m['role']}: {m['content']}" for m in chat_history]
    )