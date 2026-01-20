from Actor import Actor

class Player(Actor):
    """
    Class representing the player. Extends the Actor class, so stores player damage and health. While also adding healing
    power stat, how much the player heals when they use the healing action.
    """

    healing_power: int

    def __init__(self, health, damage, healing):
        """
        Set player health, damage, and healing power
        :param health: player health
        :param damage: player damage
        :param healing: player healing power
        """
        super().__init__(health, damage)
        self.healing_power = healing

    def heal(self):
        """
        Heals the player by healing power amount
        """
        # Check to ensure player does not heal over maximum health
        if self.current_health + self.healing_power > self.max_health:
            self.current_health = self.max_health
        else:
            self.current_health += self.healing_power

    def get_healing_power(self):
        """
        Get the healing power of the player
        :return: Healing power of player
        """
        return self.healing_power

    def increase_health(self, amount):
        """
        Increase the health of the player
        :param amount: amount to increase health
        """
        self.max_health += amount

    def increase_damage(self, amount):
        """
        Increase the damage of the player
        :param amount: amount to increase damage
        """
        self.damage += amount

    def increase_healing(self, amount):
        """
        Increase the healing power of the player
        :param amount: amount to increase healing
        """
        self.healing_power += amount

