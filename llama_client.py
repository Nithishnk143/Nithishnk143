# llama_client.py
import json
import re
import ollama


def _extract_json_block(text: str) -> str:
    """
    Extract first JSON-like block from LLM text.
    """
    # Try codefence first
    codefence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if codefence:
        return codefence.group(1)
    # Fallback: first {...}
    braces = re.search(r"\{.*\}", text, re.DOTALL)
    if braces:
        return braces.group(0)
    return text.strip()


def _safe_float(x, default=None):
    try:
        return float(x)
    except Exception:
        return default


def chat_price(
    role: str,
    context_summary: str,
    last_offer: float | None,
    constraints: dict,
    model: str = "llama3",
) -> dict:
    """
    Ask Ollama to produce a JSON:
      {"offer": <number>, "utterance": "<short message>"}
    `constraints` can include:
      - min_price, max_price, seller_floor, buyer_ceiling, currency, step_hint
    """
    sys = f"""You are an expert {role} negotiating a price.
OUTPUT RULES (IMPORTANT):
- Respond ONLY with a valid JSON object in this exact format:
  {{"offer": <number>, "utterance": "<one or two short sentences>"}}
- 'offer' MUST be a NUMBER (no commas, no currency symbol).
- Keep 'utterance' realistic, persuasive, and under 7 words.
- Never include extra text outside the JSON.
"""
    c = constraints or {}
    currency = c.get("currency", "₹")
    step_hint = c.get("step_hint", "reduce/increase sensibly per round")
    buyer_ceiling = c.get("buyer_ceiling")  # max buyer can pay
    seller_floor = c.get("seller_floor")    # min seller can accept

    # Guidance based on role
    if role == "buyer":
        hard_rule = f"NEVER go above your maximum budget (buyer_ceiling={buyer_ceiling})."
        band = f"Stay ≤ {buyer_ceiling}."
        tactic = f"Prefer {step_hint}; anchor lower than seller."
    else:
        hard_rule = f"NEVER go below your minimum acceptable price (seller_floor={seller_floor})."
        band = f"Stay ≥ {seller_floor}."
        tactic = f"Prefer {step_hint}; justify value and reduce slowly."

    user = f"""Context so far (short summary):
{context_summary}

Your role: {role}
Last seen offer: {last_offer}
Constraints: {band} {hard_rule}
Tactic hint: {tactic}
Currency (for speech only): {currency}

Return ONLY JSON with "offer" and "utterance".
"""

    resp = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": user},
        ],
        options={"temperature": 0.6},
    )

    content = resp["message"]["content"]
    raw = _extract_json_block(content)

    try:
        data = json.loads(raw)
        offer = _safe_float(data.get("offer"))
        utter = str(data.get("utterance", "")).strip()
        if offer is None:
            raise ValueError("No numeric offer")
        return {"offer": offer, "utterance": utter}
    except Exception:
        # Hard fallback: parse first number from text
        num = re.search(r"-?\d+(?:\.\d+)?", content)
        offer = float(num.group(0)) if num else (last_offer if last_offer is not None else 0.0)
        return {"offer": offer, "utterance": content.strip()[:120]}
