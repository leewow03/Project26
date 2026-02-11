class PI:
    def __init__(self, height, weight, body_fat, muscle_mass, id=None, recorded_at=None):
        self.id = id
        self.height = height
        self.weight = weight
        self.body_fat = body_fat
        self.muscle_mass = muscle_mass
        self.recorded_at = recorded_at

    @staticmethod
    def from_dict(data):
        return PI(
            id=data.get('id'),
            height=data.get('height'),
            weight=data.get('weight'),
            body_fat=data.get('body_fat'),
            muscle_mass=data.get('muscle_mass'),
            recorded_at=data.get('recorded_at')
        )