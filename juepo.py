import time

tam = 12
gato = [0, 0]
raton = [tam-1, 0]
salida = [0, tam//2]

obstaculos = {
    (tam//4,tam//4),
    (tam//4+1,tam//4),
    (tam//4,tam//4+1),
    (tam//4+1,tam-(tam//4)-1),
    (tam//4,tam-1-(tam//4)),
    (tam//4+1,tam-(tam//4)),
    (tam-(tam//4)-1,tam//4+1),
    (tam-(tam//4),tam//4+1),
    (tam-1-(tam//4),tam//4),
    (tam-4, tam-3),
    (tam-3, tam-4),
    (tam-3, tam-3)
}

DIRECCIONES = [(0,1),(1,0),(0,-1),(-1,0)] 

# ------------------------------------
# TABLERO
# ------------------------------------
def imprimir_tablero():
    print("\033[H\033[J", end="")
    for r in range(tam):
        fila = ""
        for c in range(tam):
            if [r,c] == gato:
                fila += " 🐱 "
            elif [r,c] == raton:
                fila += " 🐭 "
            elif [r,c] == salida:
                fila += " 🚪 "
            elif (r,c) in obstaculos:
                fila += " ⬛ "
            else:
                fila += " ·  "
        print(fila)
    print("\n")

# ------------------------------------
# MOVIMIENTOS VALIDOS
# ------------------------------------
def movimientos(pos):                       #pos[0] indica la fila actual y pos[1] la columna
    resultado = []                          #dr y dc los valores a sumar o restar segun el movimiento
    for dr, dc in DIRECCIONES:              #nr y nc los nuevos valores de filas y columnas
        nr, nc = pos[0] + dr, pos[1] + dc
        if (0 <= nr < tam and
            0 <= nc < tam and
            (nr, nc) not in obstaculos):
            resultado.append([nr, nc])
    return resultado

# ------------------------------------
# MOVIMIENTO HUMANO (WASD)
# ------------------------------------
def mover_humano(pos):
    tecla = input("Mover (WASD): ").lower()     #se pide el input y se transforma en minuscula

    movimientos_dict = {                        #traduccion del input a cambio en coordenadas
        "w": (-1,0),
        "s": (1,0),
        "a": (0,-1),
        "d": (0,1)
    }

    if tecla in movimientos_dict:               #Aqui se calcula la nueva posicion del jugador
        dr, dc = movimientos_dict[tecla]
        nueva = [pos[0] + dr, pos[1] + dc]
        if nueva in movimientos(pos):           #Aqui se confirma que la nueva posicion sea posible
            return nueva

    print("Movimiento inválido.")               #Se imprime un mensaje en caso de que lo anterior no se cumpla
    return pos                                  #Se queta en el mismo lugar

# ------------------------------------
# HEURISTICA
# ------------------------------------
def evaluar(gato, raton):
    dist_gato = abs(gato[0]-raton[0]) + abs(gato[1]-raton[1])
    dist_salida = abs(raton[0]-salida[0]) + abs(raton[1]-salida[1])
    return 2*dist_salida -  dist_gato

# ------------------------------------
# MINIMAX
# ------------------------------------
def minimax(gato, raton, profundidad, alpha, beta, turno_gato):

    if gato == raton:
        return 100
    if raton == salida:
        return -100
    if profundidad == 0:
        return evaluar(gato, raton)

    if turno_gato:
        mejor = -float("inf")
        for mov in movimientos(gato):
            valor = minimax(mov, raton, profundidad-1, alpha, beta, False)
            mejor = max(mejor, valor)
            alpha = max(alpha, mejor)
            if beta <= alpha:
                break
        return mejor
    else:
        peor = float("inf")
        for mov in movimientos(raton):
            valor = minimax(gato, mov, profundidad-1, alpha, beta, True)
            peor = min(peor, valor)
            beta = min(beta, peor)
            if beta <= alpha:
                break
        return peor

# ------------------------------------
# IA
# ------------------------------------
def mejor_mov_gato(profundidad):
    mejor_valor = -float("inf")
    mejor = gato
    for mov in movimientos(gato):
        valor = minimax(mov, raton, profundidad-1, -float("inf"), float("inf"), False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor = mov
    return mejor

def mejor_mov_raton(profundidad):
    mejor_valor = float("inf")
    mejor = raton
    for mov in movimientos(raton):
        valor = minimax(gato, mov, profundidad-1, -float("inf"), float("inf"), True)
        if valor < mejor_valor:
            mejor_valor = valor
            mejor = mov
    return mejor

# ------------------------------------
# JUEGO
# ------------------------------------
def jugar():
    global gato, raton

    profundidad = 4
    turno = 0
    MAX_TURNOS = 60

    print("Selecciona modo de juego:")
    print("1 - Humano (Gato) vs IA (Ratón)")
    print("2 - IA (Gato) vs Humano (Ratón)")
    print("3 - Máquina vs Máquina")

    modo = input("Opción: ")

    humano_gato = False
    humano_raton = False

    if modo == "1":
        humano_gato = True
    elif modo == "2":
        humano_raton = True
    elif modo == "3":
        pass
    else:
        print("Modo inválido. Se iniciará Máquina vs Máquina.")
    
    turno_gato = True

    while True:
        imprimir_tablero()
        print(f"Turno: {turno}")

        # Condiciones de fin
        if gato == raton:
            print("🐱 El gato ganó!")
            break

        if raton == salida:
            print("🐭 El ratón escapó!")
            break

        if turno >= MAX_TURNOS:
            print("⏳ Empate por límite de turnos.")
            break

# Turnos
        if turno_gato:
            if humano_gato:
                gato = mover_humano(gato)
            else:
                gato = mejor_mov_gato(profundidad)
        else:
            if humano_raton:
                raton = mover_humano(raton)
            else:
                raton = mejor_mov_raton(profundidad)



        turno += 1
        turno_gato = not turno_gato

        time.sleep(0.5)


# ------------------------------------
if __name__ == "__main__":
    jugar()
