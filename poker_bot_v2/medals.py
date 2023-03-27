class Medals:
    def __init__(self, gold:int, silver:int, bronze:int):
        self.gold = gold
        self.silver = silver
        self.bronze = bronze
    
    def get_gold(self) -> int:
        return self.gold
    
    def get_silver(self) -> int:
        return self.silver
    
    def get_bronze(self) -> int:
        return self.bronze
    
    def add_gold(self):
        self.gold += 1

    def add_silver(self):
        self.silver += 1

    def add_bronze(self):
        self.bronze += 1
