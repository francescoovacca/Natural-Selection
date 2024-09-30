class Food:
    def __init__(self, position: tuple):
        self.current_position = position  # coordinates of food on env grid
        self.is_eaten = False

    def __repr__(self):
        return f"(position={self.current_position}, is_eaten={self.is_eaten})\n"
