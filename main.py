import random
import tkinter as tk
from Enemy import Enemy
from Player import Player

# Initialize main Tkinter app
app = tk.Tk()
app.title("Mob Slayer 2")

# ----------------------------
# Main Menu variables
# ----------------------------
main_frame: tk.Frame

# ----------------------------
# Game variables
# ----------------------------
game_frame: tk.Frame

# ----------------------------
# Button variables
# ----------------------------
button_frame: tk.Frame

# ----------------------------
# Player Variables
# ----------------------------
player: Player
selected_enemy: int
selected_enemy_label: tk.Label
player_label: tk.Label

# ----------------------------
# Player stats (end of game display)
# ----------------------------
enemies_killed = 0
waves_cleared = 0
damage_dealt = 0
healing_received = 0

# ----------------------------
# Enemy Variables
# ----------------------------
enemies: list
enemy_frames: list
maximum_amount_of_enemies: int
wave_counter: int
enemy_image = None


def display_message(text_to_display, duration=3):
    """
    Display a message on the game screen for a limited time.

    This creates a label in the game frame and destroys it after
    'duration' seconds.

    Params:
        text_to_display (str): The message to show.
        duration (int): How long (in seconds) to show the message.
    """
    message_label = tk.Label(game_frame, text=text_to_display)
    message_label.grid(row=1, column=0)

    # Destroy message after 'duration' seconds
    message_label.after(duration * 1000, lambda: (message_label.destroy()))


def set_buttons_state(state=tk.DISABLED):
    """
    Enable or disable all buttons inside the button_frame.

    Params:
        state: tk.NORMAL or tk.DISABLED
    """
    for widget in button_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(state=state)


def new_wave():
    """
    Start a new wave and increase difficulty when needed.

    Waves cleared count increases by 1, and every 4 waves the number
    of enemies increases.
    """
    global waves_cleared, maximum_amount_of_enemies
    waves_cleared += 1

    # Give player an upgrade choice after each wave
    upgrade_stat_popup()

    # Increase enemies every 4 waves
    if waves_cleared % 4 == 0:
        maximum_amount_of_enemies += 1


def enemy_turn(index=0):
    """
    Handles enemy attacks in sequence.

    The enemies attack one by one. After all enemies attack,
    the player regains control (buttons re-enable).

    Params:
        index (int): Current enemy index attacking.
    """
    global enemies

    # If all enemies attacked, end enemy turn
    if index >= len(enemies):
        refresh_screen()
        if not enemies:
            new_wave()

        # Re-enable player buttons
        set_buttons_state(tk.NORMAL)
        return

    enemy = enemies[index]

    # Player takes damage
    player.take_damage(enemy.get_damage())

    # Display attack message
    display_message(f"Enemy dealt {enemy.get_damage()} to you!", duration=2)

    # Check for game over
    if player.get_health() <= 0:
        game_over()
        return

    refresh_screen()

    # Schedule next enemy attack
    app.after(2000, lambda: enemy_turn(index + 1))


def attack():
    """
    Player attacks the selected enemy.

    Disables buttons during the attack, updates stats, and triggers
    enemy turn afterwards.
    """
    global enemies, enemies_killed, damage_dealt

    # Disable buttons during attack
    set_buttons_state(tk.DISABLED)

    enemy = enemies[selected_enemy]
    enemy.take_damage(player.get_damage())

    # If enemy dies, remove it from the list
    if enemy.get_health() <= 0:
        display_message(f"You dealt {player.get_damage()} damage to the enemy! Killing it!", 2)
        enemies.pop(selected_enemy)
        enemy_frames.pop(selected_enemy)
        enemies_killed += 1
        damage_dealt += player.get_damage()
    else:
        display_message(f"You dealt {player.get_damage()} damage to the enemy!", 2)
        damage_dealt += player.get_damage()

    refresh_screen()

    # Wait 2 seconds then let enemies attack
    app.after(2000, enemy_turn)


def heal():
    """
    Player heals themselves.

    Heals the player by the healing power, but does not exceed max health.
    """
    global healing_received
    set_buttons_state(tk.DISABLED)

    # Get the value that is the least to display to player amount healed
    missing_health = player.get_maximum_health() - player.get_health()
    heal_amount = min(player.get_healing_power(), missing_health)

    # Heal player
    player.heal()
    healing_received += player.get_healing_power()

    display_message(f"You healed {heal_amount} health!", 2)
    refresh_screen()

    # Wait 2 seconds then let enemies attack
    app.after(2000, enemy_turn)


def game_over():
    """
    Display the game over screen and player statistics.
    """
    global game_frame
    game_frame.destroy()

    end_frame = tk.Frame(app)
    end_frame.pack()

    # Show stats
    tk.Label(end_frame, text="Game Over").pack()
    tk.Label(end_frame, text=f"Waves Cleared: {waves_cleared}").pack()
    tk.Label(end_frame, text=f"Enemies Killed: {enemies_killed}").pack()
    tk.Label(end_frame, text=f"Damage Dealt: {damage_dealt}").pack()
    tk.Label(end_frame, text=f"Healing Received: {healing_received}").pack()

    # Return to main menu button
    tk.Button(end_frame, text="Return to Main Menu",
              command=lambda: (end_frame.destroy(), main_menu())).pack()


def upgrade_stat_popup():
    """
    Opens a modal popup asking the player to choose a stat upgrade.

    The popup prevents closing until a choice is made.
    """

    def upgrade(stat):
        # Upgrade player stat based on choice
        if stat == "health":
            player.increase_health(5)
        elif stat == "damage":
            player.increase_damage(1)
        elif stat == "healing":
            player.increase_healing(2)

        popup.destroy()
        refresh_screen()
        generate_enemies()

    popup = tk.Toplevel(app)
    popup.title("Upgrade Your Stat")

    # Disable the close button (X)
    popup.protocol("WM_DELETE_WINDOW", lambda: None)

    # Make the popup modal
    popup.grab_set()

    tk.Label(popup, text="Wave Cleared!").pack()
    tk.Label(popup, text="Choose a stat to upgrade:").pack(pady=10)

    tk.Button(popup, text="Health +5", command=lambda: upgrade("health")).pack(fill="x")
    tk.Button(popup, text="Damage +1", command=lambda: upgrade("damage")).pack(fill="x")
    tk.Button(popup, text="Healing +2", command=lambda: upgrade("healing")).pack(fill="x")


def select_enemy(i):
    """
    Select which enemy the player is targeting.

    Params:
        i (int): Index of the selected enemy.
    """
    global selected_enemy
    selected_enemy = i


def on_enemy_click(event):
    """
    Handle enemy click events.

    This selects the clicked enemy and refreshes the UI.
    """
    widget = event.widget
    while widget is not None:
        if hasattr(widget, "enemy_index"):
            select_enemy(widget.enemy_index)
            refresh_screen()
            return
        widget = widget.master


def refresh_screen():
    """
    Refresh the entire game screen.

    Updates player stats, redraws enemy frames, and updates selection label.
    """
    global enemies, player, game_frame, enemy_frames, enemy_image

    # Update player stats display
    player_label.config(
        text=f"Stats - Health: {player.get_health()}/{player.get_maximum_health()} "
             f"Damage: {player.get_damage()} Healing Power: {player.get_healing_power()}"
    )

    # Clear previous enemy frames
    for frame in enemy_frames:
        frame.destroy()

    # Redraw enemy frames
    for i, enemy in enumerate(enemies):
        enemy_frame = tk.Frame(game_frame, borderwidth=2, relief="ridge")
        enemy_frame.enemy_index = i
        enemy_frame.grid(row=0, column=i, padx=5, pady=5)

        tk.Label(enemy_frame, text=f"Name: Enemy {i + 1}").grid(row=0, column=0)
        tk.Label(enemy_frame, text=f"Health: {enemy.get_health()}").grid(row=1, column=0)
        tk.Label(enemy_frame, text=f"Damage: {enemy.get_damage()}").grid(row=2, column=0)

        # IMAGE HERE
        tk.Label(enemy_frame, image=enemy_image).grid(row=3, column=0)

        # Bind click event
        enemy_frame.bind_all("<Button-1>", on_enemy_click)
        enemy_frames.append(enemy_frame)

    # Update selected enemy display
    selected_enemy_label.config(text=f"Selected Enemy = {selected_enemy + 1}")


def generate_enemies():
    """
    Generate new enemies for the current wave.

    Clears old enemies, creates new ones, and refreshes the screen.
    """
    global enemies, selected_enemy, enemy_frames, enemy_image
    enemies = []
    enemy_frames = []

    for i in range(maximum_amount_of_enemies):
        enemy_health = random.randint(1, 10)
        enemy_damage = random.randint(1, 4)
        enemy = Enemy(enemy_health, enemy_damage)
        enemies.append(enemy)

        enemy_frame = tk.Frame(game_frame, borderwidth=2, relief="ridge")
        enemy_frame.enemy_index = i
        enemy_frame.grid(row=0, column=i, padx=5, pady=5)

        tk.Label(enemy_frame, text=f"Name: Enemy {i + 1}").grid(row=0, column=0)
        tk.Label(enemy_frame, text=f"Health: {enemy.get_health()}").grid(row=1, column=0)
        tk.Label(enemy_frame, text=f"Damage: {enemy.get_damage()}").grid(row=2, column=0)

        # IMAGE HERE
        tk.Label(enemy_frame, image=enemy_image).grid(row=3, column=0)

        enemy_frame.bind_all("<Button-1>", on_enemy_click)
        enemy_frames.append(enemy_frame)

    # Reset selected enemy to first
    selected_enemy = 0
    refresh_screen()


def main_menu():
    """
    Display the main menu screen with start and tutorial buttons.
    """
    global main_frame
    main_frame = tk.Frame(app)

    label = tk.Label(main_frame, text="Mob Slayer 2")
    label.pack()

    start_button = tk.Button(main_frame, text="Start Game", command=start_game)
    start_button.pack()

    tutorial_button = tk.Button(main_frame, text="Tutorial", command=show_tutorial)
    tutorial_button.pack()

    main_frame.pack()


def show_tutorial():
    """
    Display a simple tutorial screen.

    Explains the basic controls and how to play.
    """
    global main_frame
    main_frame.destroy()

    tutorial_frame = tk.Frame(app)
    tutorial_frame.pack()

    tk.Label(tutorial_frame, text="Tutorial").pack()
    tk.Label(tutorial_frame, text="1. Click on an enemy to target it.").pack()
    tk.Label(tutorial_frame, text="2. Press Attack to damage the enemy.").pack()
    tk.Label(tutorial_frame, text="3. Press Heal to restore health.").pack()
    tk.Label(tutorial_frame, text="4. After each wave, you can upgrade one of your stats.").pack()
    tk.Label(tutorial_frame, text="5. Every three waves, one additional enemy will be added to each wave.").pack()
    tk.Label(tutorial_frame, text="6. Survive as many waves of enemies as you can!").pack()

    tk.Button(tutorial_frame, text="Back",
              command=lambda: (tutorial_frame.destroy(), main_menu())).pack()


def start_game():
    """
    Initialize the game state and build the game GUI.

    Sets player stats, loads enemy image, creates buttons, and starts the first wave.
    """
    global button_frame, player, game_frame, player_label, enemy_image, wave_counter, maximum_amount_of_enemies
    global enemies_killed, waves_cleared, damage_dealt, healing_received, selected_enemy_label, selected_enemy

    player = Player(10, 3, 5)

    maximum_amount_of_enemies = 1
    wave_counter = 0

    enemies_killed = 0
    waves_cleared = 0
    damage_dealt = 0
    healing_received = 0

    # Remove main menu frame
    main_frame.destroy()

    # Load enemy image
    enemy_image = tk.PhotoImage(file="enemy.png")

    # Create game frame
    game_frame = tk.Frame(app)

    # Player stats label
    player_label = tk.Label(
        game_frame,
        text=f"Stats - Health: {player.get_health()}/{player.get_maximum_health()} "
             f"Damage: {player.get_damage()} Healing Power: {player.get_healing_power()}"
    )
    player_label.grid(row=2, column=0, sticky=tk.SW)

    # Create buttons
    button_frame = tk.Frame(game_frame)
    button_frame.grid(row=3, column=0, sticky=tk.SW)

    attack_button = tk.Button(button_frame, text="Attack", command=attack)
    heal_button = tk.Button(button_frame, text="Heal", command=heal)
    quit_button = tk.Button(button_frame, text="Quit", command=game_over)
    attack_button.grid(row=0, column=0)
    heal_button.grid(row=0, column=1)
    quit_button.grid(row=0, column=2)

    # Enemy selection label
    selected_enemy = 0
    selected_enemy_label = tk.Label(game_frame, text=f"Selected Enemy = {selected_enemy + 1}")
    selected_enemy_label.grid(row=4, column=0)

    # Start the first wave
    generate_enemies()

    game_frame.pack()
    return


if __name__ == '__main__':
    main_menu()
    tk.mainloop()
