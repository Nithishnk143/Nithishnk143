# agents.py
from dataclasses import dataclass

@dataclass
class BuyerConfig:
    name: str
    ceiling: float          # max buyer can pay
    strategy: str = "aggressive"  # (optional tag)


@dataclass
class SellerConfig:
    name: str
    floor: float            # min seller can accept
    strategy: str = "flexible"    # (optional tag)


class Buyer:
    def __init__(self, cfg: BuyerConfig):
        self.cfg = cfg

    @property
    def name(self):
        return self.cfg.name

    def constraints(self):
        return {
            "buyer_ceiling": self.cfg.ceiling,
            "step_hint": "reduce in 2–10% steps",
            "currency": "₹",
        }


class Seller:
    def __init__(self, cfg: SellerConfig):
        self.cfg = cfg

    @property
    def name(self):
        return self.cfg.name

    def constraints(self):
        return {
            "seller_floor": self.cfg.floor,
            "step_hint": "concede in 1–8% steps",
            "currency": "₹",
        }
