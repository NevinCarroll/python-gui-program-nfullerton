class Actor:
    """
    This class stores information about actors in the game (ex. player, enemy) These stats include, current health, max
    health, and damage.
    """
    current_health: int
    max_health: int
    damage: int

    def __init__(self, health: int, damage: int):
        """
        Sets the stats of the actor
        :param health: Maximum health of the actor
        :param damage: Damage of the actor
        """
        self.current_health = health
        self.max_health = health
        self.damage = damage

    def take_damage(self, damage: int):
        """
        Lowers the health of the actor by the damage
        :param damage: Damage taken
        """
        self.current_health -= damage

    def get_health(self) -> int:
        """
        Get the health of the actor
        :return: health of the actor
        """
        return self.current_health

    def get_maximum_health(self) -> int:
        """
        Get the maximum health of the actor
        :return: Maximum health of the actor
        """
        return self.max_health

    def get_damage(self) -> int:
        """
        Get the damage amount of the actor
        :return: damage amount
        """
        return self.damage