from random import randint, choices
import numpy as np
import math

def display_letter(value):
    if value == 0:
        return '.'
    power = int(math.log2(value))
    return chr(power - 1 + ord('A'))


def rand(matrix):
    value = [2, 4]
    prob = [0.9, 0.1]
    val_prob = choices(value, prob, k=1)[0]

    empty_positions = [(i, j) for i in range(4) for j in range(4) if matrix[i][j] == 0]
    if not empty_positions:
        return

    i0, j0 = empty_positions[randint(0, len(empty_positions) - 1)]
    matrix[i0][j0] = val_prob



def W(matrix):
    global score
    moved = False
    for j in range(4):
        for i in range(1, 4):
            if matrix[i][j] != 0:
                n = i
                i0 = i - 1
                while i0 >= 0:
                    if matrix[i0][j] == 0:
                        matrix[i0][j] = matrix[n][j]
                        matrix[n][j] = 0
                        i0 -= 1
                        n -= 1
                        moved = True
                    elif matrix[i0][j] == matrix[n][j]:
                        matrix[i0][j] *= 2
                        score += matrix[i0][j]
                        matrix[n][j] = 0
                        moved = True
                        break
                    else:
                        break
    return moved


def S(matrix):
    global score
    moved = False
    for j in range(4):
        for i in reversed(range(3)):
            if matrix[i][j] != 0:
                n = i
                i0 = i + 1
                while i0 <= 3:
                    if matrix[i0][j] == 0:
                        matrix[i0][j] = matrix[n][j]
                        matrix[n][j] = 0
                        i0 += 1
                        n += 1
                        moved = True
                    elif matrix[i0][j] == matrix[n][j]:
                        matrix[i0][j] *= 2
                        score += matrix[i0][j]
                        matrix[n][j] = 0
                        moved = True
                        break
                    else:
                        break
    return moved


def D(matrix):
    global score
    a = matrix.transpose()
    moved = False
    for j in range(4):
        for i in reversed(range(3)):
            if a[i][j] != 0:
                n = i
                i0 = i + 1
                while i0 <= 3:
                    if a[i0][j] == 0:
                        a[i0][j] = a[n][j]
                        a[n][j] = 0
                        i0 += 1
                        n += 1
                        moved = True
                    elif a[i0][j] == a[n][j]:
                        a[i0][j] *= 2
                        score += a[i0][j]
                        a[n][j] = 0
                        moved = True
                        break
                    else:
                        break
    matrix[:] = a.transpose()
    return moved


def A(matrix):
    global score
    a = matrix.transpose()
    moved = False
    for j in range(4):
        for i in range(1, 4):
            if a[i][j] != 0:
                n = i
                i0 = i - 1
                while i0 >= 0:
                    if a[i0][j] == 0:
                        a[i0][j] = a[n][j]
                        a[n][j] = 0
                        i0 -= 1
                        n -= 1
                        moved = True
                    elif a[i0][j] == a[n][j]:
                        a[i0][j] *= 2
                        score += a[i0][j]
                        a[n][j] = 0
                        moved = True
                        break
                    else:
                        break
    matrix[:] = a.transpose()
    return moved



def can_move(matrix):
    if any(0 in row for row in matrix):
        return True

    for i in range(4):
        for j in range(3):
            if matrix[i][j] == matrix[i][j + 1]:
                return True

    for j in range(4):
        for i in range(3):
            if matrix[i][j] == matrix[i + 1][j]:
                return True

    return False



try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except:
    highscore = 0


print("Commands are as follows:")
print("'W','w': Move Up\n'S','s': Move Down\n'A','a': Move Left\n'D','d': Move Right")


while True:
    score = 0

    matrix = np.array([[0, 2, 2, 4],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 2, 0]])

    rand(matrix)

    while True:
        print(f"\nScore: {score}   Highscore: {highscore}\n")

        for row in matrix:
            print(' '.join(f"{display_letter(num):5}" for num in row))

        inp = input("\nPress the command: ").lower()

        if inp not in ['w', 'a', 's', 'd']:
            print("Not in commands")
            continue

        if 2**26 in matrix:
            print("\nYou have reached Z! You won! ðŸŽ‰")
            break

        if not can_move(matrix):
            print("\nYou have lost :(")
            break

        if inp == 'w':
            moved = W(matrix)
        elif inp == 's':
            moved = S(matrix)
        elif inp == 'a':
            moved = A(matrix)
        elif inp == 'd':
            moved = D(matrix)

        if moved:
            rand(matrix)
        else:
            print("Move not possible, try a different direction.")

    if score > highscore:
        highscore = score
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))
        print("New Highscore Saved!")

    while True:
        play = input("\nDo you want to play again (yes/no): ").lower()
        if play in ['yes', 'y']:
            break
        elif play in ['no', 'n']:
            print("Good Bye!")
            exit()
        else:
            print("Invalid input please input yes or no:")



