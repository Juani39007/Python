Retos
1. Límites de pantalla

Cómo funciona: el jugador es un rectángulo. Después de moverlo, si se ha salido de la ventana, se vuelve a meter dentro. Pasa por los cuatro lados y con los dos jugadores.
Cómo lo he hecho: en player.py, al final de moveArrows y de moveWASD.

python
self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))  # Keep the player inside the window

pygame.Rect(0, 0, WIDTH, HEIGHT) es un rectángulo del tamaño de la ventana. clamp_ip obliga al rectángulo del jugador a quedarse dentro de él. Por ejemplo, si el jugador está en x = 790 y mide 50, lo deja en x = 750.

2. Tamaños aleatorios

Cómo funciona: cada obstáculo nace con un tamaño distinto, entre 20 y 70 píxeles, y siempre cabe entero en el ancho de la ventana.
Cómo lo he hecho: en obstacle.py, en el __init__.

python
size = random.randint(20, 70)  # Random size between 20 and 70 pixels
x = random.randint(0, WIDTH - size)

Un rectángulo se coloca por su esquina izquierda. Si un obstáculo de 70 empezara en x = 780, ocuparía hasta 850 y se saldría de la ventana (que mide 800). Por eso la x máxima es WIDTH - size.

3. Colisión con el jugador 2

Cómo funciona: un obstáculo que toca a cualquiera de los dos jugadores le afecta, no solo al primero.
Cómo lo he hecho: en main.py se comprueba el choque con los dos jugadores.

python
if player.rect.colliderect(obstacle.rect) or player2.rect.colliderect(obstacle.rect):
    game_over = True

colliderect devuelve True si dos rectángulos se tocan. El or hace que baste con que choque uno de los dos. En la versión final, con las vidas, esto está dentro del bucle del reto 10.

4. Pausa

Cómo funciona: ESC para el juego y vuelve a ponerlo en marcha. En pausa no se mueve nada, no salen obstáculos y aparece el texto PAUSE.
Cómo lo he hecho: en main.py, con la variable paused.

python
if event.key == pygame.K_ESCAPE and not game_over:
    paused = not paused  # Pause / continue
python
if not game_over and not paused:
    # ... everything that moves or creates things is here ...
python
if paused:
    pause_text = font.render("PAUSE", True, (255, 255, 255))
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

paused = not paused cambia entre True y False cada vez que se pulsa ESC. Todo lo que mueve o crea cosas está dentro del if not game_over and not paused, así que en pausa ese bloque no se ejecuta. El dibujo está fuera, por eso se sigue viendo la pantalla con el mensaje.

5. Reiniciar la partida

Cómo funciona: cuando sale Game Over, R empieza otra partida sin cerrar el programa, con la puntuación a cero, sin obstáculos y con los jugadores en su sitio.
Cómo lo he hecho: con la función reset_game() de main.py.

python
def reset_game():
    """Start a new game (the high score is kept)"""
    global player, player2, obstacles, score, game_over, survival_time
    global powerups, last_powerup_spawn_time

    player = Player(375, 530)
    player2 = Player(100, 100, PLAYER_COLOR2, 2)
    obstacles = []
    score = 0
    survival_time = 0
    game_over = False
    powerups = []
    last_powerup_spawn_time = 0
python
if event.key == pygame.K_r and game_over and not entering_name:
    reset_game()  # Restart after Game Over

La función vuelve a crear los jugadores en sus posiciones de salida y deja todo a cero. Lleva global porque esas variables están fuera de la función. No toca high_score, por eso el récord se mantiene.

6. Tiempo de supervivencia

Cómo funciona: en pantalla se ven los segundos que llevas vivo. El contador se para en pausa y en Game Over.
Cómo lo he hecho: en main.py, sumando el tiempo de cada vuelta del bucle.

python
# The survival time only grows while the game is running
now = pygame.time.get_ticks()
if not game_over and not paused:
    survival_time += now - last_tick
last_tick = now
python
time_text = font.render(f"Time: {survival_time // 1000}", True, (255, 255, 255))

get_ticks() cuenta los milisegundos desde que arrancó el programa y no se detiene nunca, ni en pausa. Por eso en cada vuelta miro cuánto ha pasado desde la anterior (now - last_tick) y solo lo sumo si el juego está en marcha. // 1000 pasa los milisegundos a segundos.

7. Dificultad progresiva

Cómo funciona: cuantos más puntos, más seguido salen los obstáculos: 50 ms menos cada 10 puntos, sin bajar de 150 ms.
Cómo lo he hecho: con la función get_spawn_delay de main.py.

python
def get_spawn_delay(current_score):
    """Every 10 points the delay is 50 ms shorter, never below the minimum"""
    delay = SPAWN_OBSTACLE_DELAY - (current_score // 10) * 50
    return max(delay, MIN_SPAWN_DELAY)

current_score // 10 es el nivel (con 25 puntos, 2). Cada nivel resta 50 al intervalo inicial de 500, así que con 25 puntos son 400 ms. El max impide que baje de 150.

8. Cambiar velocidad

Cómo funciona: + sube y - baja la velocidad del jugador 1, entre 2 y 12, y cada pulsación cuenta una sola vez.
Cómo lo he hecho: change_speed en player.py y las teclas en main.py.

python
def change_speed(self, amount):
    """Change the speed, always between the minimum and the maximum"""
    self.speed = max(MIN_PLAYER_SPEED, min(MAX_PLAYER_SPEED, self.speed + amount))
python
if event.key == pygame.K_PLUS:
    player.change_speed(1)  # Speed up player 1
if event.key == pygame.K_MINUS:
    player.change_speed(-1)  # Slow down player 1

El min evita pasar de 12 y el max evita bajar de 2. Las teclas se leen con KEYDOWN, que salta una vez por pulsación. Con get_pressed() cambiaría en cada frame mientras la tecla siguiera pulsada.

9. Récord de puntuación

Cómo funciona: al lado de la puntuación se ve la mejor de la sesión. Al reiniciar, la puntuación vuelve a cero pero el récord se queda.
Cómo lo he hecho: con la variable high_score en main.py.

python
if score > high_score:
    high_score = score  # Remember the best score
python
score_text = font.render(f"Score: {score}   Best: {high_score}", True, (255, 255, 255))

high_score se crea una sola vez al empezar el programa y solo cambia cuando la puntuación la supera. reset_game no la toca, así que sobrevive a los reinicios.


[enlace a gameplay](assets/gameplay.mp4)
