from prettytable import PrettyTable
from PIL import Image, ImageDraw
from subprocess import Popen
import platform
import pygame
import numpy as np

def main():
    # Problem 1
    print("Problem 1:")
    subsets()

    # Problem 2
    print("\nProblem 2:")
    XNOR()

    # Problem 3
    print("\nProblem 3:")
    next_integer()

    # Problem 4
    print("\nProblem 4:")
    truth_table_solver()

    # Problem 5
    print("\nProblem 5:")
    sierpinski_carpet()

    # Problem 6
    print("\nProblem 6:")
    a_game_of_life_foreplay()

def subsets():
    nums = list(map(int, input("Enter the set: ").split()))
    power_set = [[]]
    for i in range(len(nums)):
        for j in range(len(power_set)):
            power_set.append([*power_set[j], nums[i]])
    print("Result: " + str(power_set))

def XNOR():
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    print("Result: " + str(int((a and b) or (not a and not b))))

def next_integer():
    n = input("Enter a number: ")
    digits = list(str(n))
    i = len(digits) - 2
    while i >= 0 and digits[i] <= digits[i+1]:
        i -= 1
    if i == -1:
        return n
    j = len(digits) - 1
    while digits[j] >= digits[i]:
        j -= 1
    digits[i], digits[j] = digits[j], digits[i]
    digits[i+1:] = sorted(digits[i+1:])
    result = int("".join(digits))
    print("Result: " + str(result))

def truth_table_solver():
    org_exp  = input("Your expression: ")
    variables = {}
    for e in list(org_exp):
        if e.isalpha():
            variables[e] = []
    exp = org_exp.replace('+', ' or ')
    exp = exp.replace('*', ' and ')
    exp = exp.replace('!', ' not ')

    num_vars = len(variables)
    num_combinations = 2 ** len(variables)

    for i in range(num_combinations):
        binary = f'{i:0{num_vars}b}'
        bin = str(binary)
        j = 0
        for key in variables:
            variables[key].append(int(bin[j]))
            j += 1

    results = []
    for i in range(num_combinations):
        new_exp = exp
        for key in variables:
            new_exp = new_exp.replace(key, str(variables[key][i]))
        results.append(int(eval(new_exp)))

    table = PrettyTable()


    for key in variables:
        table.field_names.append(key)
        table.align[key] = 'l'
        table.valign[key] = 'm'
    table.field_names.append(org_exp)
    table.align[org_exp] = 'l'
    table.valign[org_exp] = 'm'

    for i in range(num_combinations):
        row = []
        for key in variables:
            row.append(variables[key][i])
        row.append(results[i])
        table.add_row(row)

    print(table)

def sierpinski_carpet():
    n = int(input("How many recursions: "))
    size = 3**n
    total_operations = (8**n - 1) / 7
    done_operations = 0
    persentage = 0
    print("Progress: 0%")
    carpet = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(carpet)
    draw.rectangle([0, 0, size, size], fill='black')


    def holify(start_x, start_y, end_x, end_y, n):
        nonlocal done_operations
        nonlocal persentage
        n -= 1
        if n < 0:
            return
        diff = (end_x - start_x)/3
        hole_start_x = start_x + diff
        hole_start_y = start_y + diff
        hole_end_x = end_x - diff - 1
        hole_end_y = end_y - diff - 1
        draw.rectangle([hole_start_x, hole_start_y, hole_end_x, hole_end_y], fill='white')
        done_operations += 1
        new_persentage = int((done_operations/total_operations)*100)
        if new_persentage != persentage:
            persentage = new_persentage
            print("Progress: "+str(persentage)+"%")
            
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                recursive_start_x = start_x + diff*i
                recursive_start_y = start_y + diff*j
                recursive_end_x = recursive_start_x + diff
                recursive_end_y = recursive_start_y + diff
                holify(recursive_start_x, recursive_start_y, recursive_end_x, recursive_end_y, n)

    holify(0, 0, size, size, n)
    carpet.save("carpet.png")
    carpet.show()

def a_game_of_life_foreplay():
    WIDTH, HEIGHT = 800, 600
    CELL_SIZE = 5
    GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
    WHITE, BLACK = (255, 255, 255), (0, 0, 0)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    grid = np.random.choice([0, 1], (GRID_WIDTH, GRID_HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        new_grid = grid.copy()

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                neighbors = np.sum(grid[x - 1:x + 2, y - 1:y + 2]) - grid[x, y]

                if grid[x, y] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[x, y] = 0
                else:
                    if neighbors == 3:
                        new_grid[x, y] = 1

        grid = new_grid
        screen.fill(WHITE)
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if grid[x, y]:
                    pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(10)
main()