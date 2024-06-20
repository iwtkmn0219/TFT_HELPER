class Champion:
    def __init__(self, name: str, cost: int, star: int, value: list) -> None:
        self.name = name
        self.cost = cost
        self.star = star
        self.value = value

    def __repr__(self) -> str:
        return f"cost: {self.cost}, name: {self.name}, star: {self.star}, value: {self.value}"

    def to_dict(self):
        return {"name": self.name, "cost": self.cost, "star": self.star}
