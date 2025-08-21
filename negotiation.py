import random
import ollama  # Make sure ollama is installed and running

class NegotiationAI:
    def __init__(self, product, seller_price, buyer_price, max_rounds=10):
        self.product = product
        self.seller_price = seller_price
        self.buyer_price = buyer_price
        self.max_rounds = max_rounds

    def get_chat_response(self, role, offer, context):
        """Generate buyer/seller messages dynamically from Ollama"""
        prompt = f"""
        You are playing the role of a {role} in a product price negotiation.
        Product: {self.product}
        Your current {role} offer is exactly ₹{offer}.
        Context: {context}

        IMPORTANT RULE: You MUST always mention the exact amount ₹{offer}
        (do NOT invent or change numbers).
        Keep the reply short and casual (you can use emojis).     """
        try:
            response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
            return response["message"]["content"].strip()
        except Exception as e:
            return f"(⚠️ Fallback) {role} says: Let's discuss more."

    def smart_negotiation(self):
        print(f"\n🛒 Negotiation starts for: {self.product}\n")
        print(f"(Starting) Buyer asking: ₹{self.buyer_price} | Seller initial price: ₹{self.seller_price}\n")

        buyer_offer = self.buyer_price
        seller_offer = self.seller_price

        for round_no in range(1, self.max_rounds + 1):
            print(f"--- Round {round_no} ---")

            # Buyer message from Ollama
            buyer_msg = self.get_chat_response("buyer", buyer_offer, "Wants lowest possible price")
            print(f"Buyer: {buyer_msg} | Offer: ₹{buyer_offer}")

            if buyer_offer >= seller_offer:
                print(f"✅ Deal closed at ₹{buyer_offer} 🎉\n")
                return

            # Seller message from Ollama
            seller_msg = self.get_chat_response("seller", seller_offer, "Wants maximum profit")
            print(f"Seller: {seller_msg} | Counter: ₹{seller_offer}\n")

            # Update offers
            buyer_offer += random.randint(500, 2000)
            seller_offer -= random.randint(500, 1500)

            if buyer_offer >= seller_offer:
                final_price = (buyer_offer + seller_offer) // 2
                print(f"✅ Deal finalized at ₹{final_price} 🎉\n")
                return

        print("❌ Negotiation failed, no deal reached.\n")
