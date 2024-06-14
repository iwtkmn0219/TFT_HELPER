class Champion:
    def __init__(self, name: str, cost: int, star: int) -> None:
        self.name = name
        self.cost = cost
        self.star = star

    def __repr__(self) -> str:
        return f"{self.cost} {self.name} {'★' * self.star}"

    def to_dict(self):
        return {"name": self.name, "cost": self.cost, "star": self.star}
