chat_session= {} 
MAX_MESSAGES = 8

def get_session(session_id):
    return chat_session.setdefault(
        session_id,
        {"summary":"", "messages":[]}
    )


def add_message(session_id, role, content):
    session = get_session(session_id)
    session["messages"].append(
        {"role":role, "content":content}
    )
    
def summarize_messages(llm, messages, old_summary=""):
    
    text = "\n".join(
        f"{m['role']}: {m['content']} " for m in messages
        
        
    )    
    prompt = f"""
        You are a memory summarizer.

        Existing summary:
        {old_summary}

        New conversation:
        {text}

        Update the summary concisely.
        """
        
    return llm.invoke(prompt).content

def maybe_summarize(session_id, llm):
    session = get_session(session_id)

    if len(session["messages"]) > MAX_MESSAGES:
        old_messages = session["messages"][:-4]
        recent_messages = session["messages"][-4:]

        session["summary"] = summarize_messages(
            llm,
            old_messages,
            session["summary"]
        )

        session["messages"] = recent_messages
        
        
def build_prompt(session_id, question):
    session = get_session(session_id)

    messages = []

    if session["summary"]:
        messages.append({
            "role": "system",
            "content": f"Conversation summary:\n{session['summary']}"
        })

    messages.extend(session["messages"])
    messages.append({"role": "user", "content": question})

    return messages

