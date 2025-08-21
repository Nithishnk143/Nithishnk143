import ollama

def generate_dialogue(agent_name: str, role: str, strategy: str, offer: float, prev_offer: float) -> str:
    """
    Use Ollama to generate a bluffing / negotiation dialogue line.
    """
    prompt = f"""
    You are {agent_name}, a {role} in a price negotiation.
    Your personality is {strategy}.
    Current offer on table: {prev_offer}
    You are proposing: {offer}
    Respond with ONE short sentence in character (like a human negotiator),
    no explanation, only dialogue.
    """
    try:
        response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"].strip()
    except Exception as e:
        return f"[{agent_name}] offers {offer} (no AI response, error: {e})"
