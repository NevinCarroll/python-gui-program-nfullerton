from Actor import Actor

class Enemy(Actor):
    """
    Class representing the enemy the play fights. Currently, has no additional functionality besides base Actor class
    methods.
    """

    def __init__(self, health, damage):
        """
        Set up enemy health and damage.
        :param health: enemy health
        :param damage: enemy damage
        """
        super().__init__(health, damage)


