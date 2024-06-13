class Comp:
    def __init__(self, name: str, champions: list):
        self.name = name
        self.champions = champions

    def __repr__(self) -> str:
        return f"[name: {self.name}, champions: {self.champions}]"

    def to_dict(self) -> None:
        return {"name": self.name, "champions": self.champions}
