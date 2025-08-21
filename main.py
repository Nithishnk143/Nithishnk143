from negotiation import NegotiationAI

if __name__ == "__main__":
    product = "iPhone 15 Pro"
    seller_price = 120000
    buyer_price = 60000

    bot = NegotiationAI(product, seller_price, buyer_price)
    bot.smart_negotiation()
