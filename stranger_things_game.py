
import tkinter as tk
import random

# STRANGER THINGS: ESCAPE FROM THE UPSIDE DOWN
# No external packages required. Run with: python stranger_things_game.py

W, H = 900, 600
root = tk.Tk()
root.title("Stranger Things: Escape from the Upside Down")
root.resizable(False, False)

canvas = tk.Canvas(root, width=W, height=H, bg="#08050d", highlightthickness=0)
canvas.pack()

# Game state
state = "menu"
score = 0
health = 100
has_flashlight = False
has_key = False
gate_open = False
message = ""
keys_down = set()
enemy_dx = 2.0
enemy_dy = 1.5

player = {"x": 120, "y": 470, "r": 16}
enemy = {"x": 700, "y": 180, "r": 22}
items = {
    "flashlight": {"x": 220, "y": 150, "taken": False},
    "key": {"x": 480, "y": 400, "taken": False},
}
gate = {"x": 820, "y": 300, "w": 35, "h": 120}

def reset():
    global score, health, has_flashlight, has_key, gate_open, message, state
    score = 0
    health = 100
    has_flashlight = False
    has_key = False
    gate_open = False
    message = "Find the flashlight, then find the key. Escape through the gate!"
    player.update(x=120, y=470)
    enemy.update(x=700, y=180)
    for v in items.values():
        v["taken"] = False
    state = "playing"

def text(x, y, s, size=18, fill="#eeeeee", anchor="center"):
    canvas.create_text(x, y, text=s, fill=fill, font=("Consolas", size, "bold"),
                       anchor=anchor)

def draw_menu():
    canvas.delete("all")
    # fog / stars
    for _ in range(80):
        x = random.randint(0, W)
        y = random.randint(0, H)
        canvas.create_oval(x, y, x+2, y+2, fill="#321638", outline="")
    text(W/2, 115, "STRANGER THINGS", 42, "#e71d36")
    text(W/2, 165, "ESCAPE FROM THE UPSIDE DOWN", 23, "#b7b0c8")
    text(W/2, 270, "You are trapped in the Upside Down.", 18)
    text(W/2, 305, "Find the flashlight. Find the key.", 18)
    text(W/2, 340, "Avoid the DEMOGORGON and reach the gate.", 18)
    canvas.create_rectangle(330, 405, 570, 465, fill="#1b1025", outline="#e71d36", width=3)
    text(W/2, 435, "PRESS ENTER TO START", 19, "#ffffff")
    text(W/2, 540, "Arrow keys / WASD = Move    |    R = Restart", 14, "#817a91")

def draw_game():
    canvas.delete("all")

    # Background
    canvas.create_rectangle(0, 0, W, H, fill="#09060f", outline="")
    # Red lightning / vines
    for i in range(0, W, 90):
        pts = [i, 0]
        x = i
        for y in range(35, H, 55):
            x += random.choice([-25, -10, 10, 25])
            pts += [x, y]
        canvas.create_line(*pts, fill="#3a122f", width=3)

    # Ground
    canvas.create_rectangle(25, 70, W-25, H-25, outline="#351d3d", width=3)

    # Gate
    gx, gy, gw, gh = gate["x"], gate["y"], gate["w"], gate["h"]
    gate_color = "#37e6a5" if gate_open else "#e71d36"
    canvas.create_rectangle(gx, gy, gx+gw, gy+gh, outline=gate_color, width=6)
    text(gx+gw/2, gy-20, "EXIT", 12, gate_color)

    # Items
    if not items["flashlight"]["taken"]:
        x, y = items["flashlight"]["x"], items["flashlight"]["y"]
        canvas.create_oval(x-12, y-12, x+12, y+12, fill="#f5e663", outline="#fff5a8", width=2)
        text(x, y+28, "FLASHLIGHT", 10, "#f5e663")
    if not items["key"]["taken"]:
        x, y = items["key"]["x"], items["key"]["y"]
        canvas.create_oval(x-10, y-10, x+10, y+10, fill="#e8c45b", outline="#fff0a0", width=2)
        canvas.create_line(x+8, y, x+25, y, fill="#e8c45b", width=4)
        text(x, y+25, "KEY", 10, "#e8c45b")

    # Enemy
    ex, ey, er = enemy["x"], enemy["y"], enemy["r"]
    canvas.create_oval(ex-er, ey-er, ex+er, ey+er, fill="#35101e", outline="#e71d36", width=3)
    canvas.create_oval(ex-10, ey-8, ex-4, ey-2, fill="#ff3b58", outline="")
    canvas.create_oval(ex+4, ey-8, ex+10, ey-2, fill="#ff3b58", outline="")
    canvas.create_line(ex-12, ey+8, ex, ey+15, ex+12, ey+8, fill="#e71d36", width=3)
    text(ex, ey+35, "DEMOGORGON", 10, "#e71d36")

    # Player
    px, py, pr = player["x"], player["y"], player["r"]
    canvas.create_oval(px-pr, py-pr, px+pr, py+pr, fill="#4da6ff", outline="#d7efff", width=2)
    text(px, py, "●", 12, "#ffffff")

    # HUD
    canvas.create_rectangle(0, 0, W, 58, fill="#110b18", outline="#3d2846")
    text(18, 18, "HEALTH", 11, "#aaa0b2", anchor="w")
    canvas.create_rectangle(75, 11, 275, 31, outline="#5b405f")
    canvas.create_rectangle(75, 11, 75 + max(0, 200*health/100), 31,
                            fill="#e71d36", outline="")
    text(290, 21, f"{health}/100", 12, "#ffffff", anchor="w")
    text(430, 20, f"SCORE: {score}", 13, "#f5e663")
    inv = ("🔦 " if has_flashlight else "") + ("🔑 " if has_key else "")
    text(600, 20, "INVENTORY: " + (inv or "empty"), 12, "#b7e9ff", anchor="w")
    text(18, 75, message, 12, "#d7cde0", anchor="w")

    text(W/2, H-10, "Move: WASD / Arrow Keys    |    R: Restart", 11, "#756b7d")

def distance(a, b):
    return ((a["x"]-b["x"])**2 + (a["y"]-b["y"])**2) ** 0.5

def move_player():
    speed = 4
    dx = dy = 0
    if "left" in keys_down or "a" in keys_down: dx -= speed
    if "right" in keys_down or "d" in keys_down: dx += speed
    if "up" in keys_down or "w" in keys_down: dy -= speed
    if "down" in keys_down or "s" in keys_down: dy += speed

    player["x"] = max(45, min(W-55, player["x"] + dx))
    player["y"] = max(85, min(H-50, player["y"] + dy))

def move_enemy():
    global enemy_dx, enemy_dy
    # Slowly chase the player
    if enemy["x"] < player["x"]: enemy["x"] += 0.75
    else: enemy["x"] -= 0.75
    if enemy["y"] < player["y"]: enemy["y"] += 0.65
    else: enemy["y"] -= 0.65

    # Small wandering variation
    enemy["x"] += enemy_dx * 0.18
    enemy["y"] += enemy_dy * 0.18
    if enemy["x"] < 80 or enemy["x"] > 780: enemy_dx *= -1
    if enemy["y"] < 100 or enemy["y"] > 500: enemy_dy *= -1

def update():
    global health, score, message, gate_open, state, has_flashlight, has_key

    if state == "playing":
        move_player()
        move_enemy()

        # Pickups
        if not items["flashlight"]["taken"] and distance(player, items["flashlight"]) < 35:
            items["flashlight"]["taken"] = True
            has_flashlight = True
            score += 100
            message = "You found the flashlight! The darkness is no longer hiding everything..."

        if not items["key"]["taken"] and distance(player, items["key"]) < 35:
            items["key"]["taken"] = True
            has_key = True
            score += 150
            message = "You found the gate key! Now reach the EXIT."

        gate_open = has_key

        # Enemy collision
        if distance(player, enemy) < 38:
            health -= 1.5
            message = "THE DEMOGORGON IS CLOSE! RUN!"
            if health <= 0:
                health = 0
                state = "gameover"
        elif has_flashlight and distance(player, enemy) < 150:
            # Flashlight pushes enemy away
            dx = enemy["x"] - player["x"]
            dy = enemy["y"] - player["y"]
            d = max(1, (dx*dx + dy*dy)**0.5)
            enemy["x"] += dx/d * 2
            enemy["y"] += dy/d * 2

        # Escape
        if gate_open and player["x"] > gate["x"]-15 and gate["y"] < player["y"] < gate["y"]+gate["h"]:
            score += int(health * 2)
            state = "win"

    draw()

    root.after(30, update)

def draw():
    if state == "menu":
        draw_menu()
    elif state == "playing":
        draw_game()
    elif state == "gameover":
        draw_game()
        canvas.create_rectangle(170, 190, 730, 410, fill="#120813", outline="#e71d36", width=4)
        text(W/2, 245, "THE UPSIDE DOWN GOT YOU", 28, "#e71d36")
        text(W/2, 295, f"Final score: {score}", 18)
        text(W/2, 340, "Press R to try again", 16, "#f5e663")
    elif state == "win":
        draw_game()
        canvas.create_rectangle(140, 170, 760, 430, fill="#0b1715", outline="#37e6a5", width=4)
        text(W/2, 225, "YOU ESCAPED!", 38, "#37e6a5")
        text(W/2, 280, "The gate slammed shut behind you.", 18)
        text(W/2, 315, f"Final score: {score}", 20, "#f5e663")
        text(W/2, 365, "Press R to play again", 16)

def key_down(event):
    global state
    k = event.keysym.lower()
    if state == "menu" and k == "return":
        reset()
    elif k in ("left","right","up","down","w","a","s","d"):
        keys_down.add(k)
    elif k == "r":
        reset()

def key_up(event):
    keys_down.discard(event.keysym.lower())

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

draw()
update()
root.mainloop()
