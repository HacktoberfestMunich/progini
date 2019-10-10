import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
(screen_width, screen_height) = (pygame.display.Info().current_w, pygame.display.Info().current_h)

lines = []
lineColors = []
lineThicknesses = []

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
colorList = [black, red, green, blue]
currentColor = black

initialLineThickness = 5
currentThickness = initialLineThickness

drawing = False
drawingModeChanged = False

lastMovementTime = pygame.time.get_ticks()
lastMousePos = (0, 0)
minMouseMovement = 10

pygame.mouse.get_rel()

font = pygame.font.SysFont("arial", 72)
text = font.render("Not Drawing", True, (0, 128, 0))
plusText = font.render("+", True, black)
minusText = font.render("-", True, black)
plusRect = pygame.Rect(100, screen_height - 100, 100, 100)
minusRect = pygame.Rect(0, screen_height - 100, 100, 100)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    screen.fill(white)
    screen.blit(text, (0, 0, text.get_width(), text.get_height()))

    for col in colorList:
        colorRect = (screen_width - (screen_height / len(colorList)), screen_height / len(colorList) * colorList.index(col), (screen_height / len(colorList)), (screen_height / len(colorList)))
        pygame.draw.rect(screen, col, colorRect)

    pygame.draw.rect(screen, black, minusRect, initialLineThickness)
    pygame.draw.rect(screen, black, plusRect, initialLineThickness)

    screen.blit(minusText, minusRect)
    screen.blit(plusText, plusRect)

    if abs(pygame.mouse.get_rel()[0]) >= minMouseMovement or abs(pygame.mouse.get_rel()[1]) >= minMouseMovement:
        lastMovementTime = pygame.time.get_ticks()
        drawingModeChanged = False

    if (not drawingModeChanged) and (pygame.time.get_ticks() - lastMovementTime >= 1000):
        if pygame.mouse.get_pos()[0] > screen_width - (screen_height / len(colorList)):
            currentColor = screen.get_at(pygame.mouse.get_pos())
            if drawing:
                text = font.render("Drawing\n({}, {}, {})\n{}".format(currentColor[0], currentColor[1], currentColor[2], currentThickness), True, currentColor)
            else:
                text = font.render("Not drawing\n({}, {}, {})\n{}".format(currentColor[0], currentColor[1], currentColor[2], currentThickness), True, currentColor)
        elif minusRect.collidepoint(pygame.mouse.get_pos()):
            if currentThickness > initialLineThickness:
                currentThickness -= 1
            if drawing:
                text = font.render("Drawing\n({}, {}, {})\n{}".format(currentColor[0], currentColor[1], currentColor[2], currentThickness), True, currentColor)
            else:
                text = font.render("Not drawing\n({}, {}, {})\n{}".format(currentColor[0], currentColor[1], currentColor[2], currentThickness), True, currentColor)
        elif plusRect.collidepoint(pygame.mouse.get_pos()):
            currentThickness += 1
            if drawing:
                text = font.render("Drawing\n({}, {}, {})\n{}".format(currentColor[0], currentColor[1], currentColor[2], currentThickness), True, currentColor)
            else:
                text = font.render("Not drawing\n({}, {}, {})\n{}".format(currentColor[0], currentColor[1], currentColor[2], currentThickness), True, currentColor)
        else:
            drawing = not drawing
            drawingModeChanged = True
            if drawing:
                text = font.render("Drawing\n({}, {}, {})\n{}".format(currentColor[0], currentColor[1], currentColor[2], currentThickness), True, currentColor)
                lines.append([])
                lineColors.append(currentColor)
                lineThicknesses.append(currentThickness)
            else:
                text = font.render("Not drawing\n({}, {}, {})\n{}".format(currentColor[0], currentColor[1], currentColor[2], currentThickness), True, currentColor)

    if drawing:
        lines[-1].append(pygame.mouse.get_pos())

    for points in lines:
        lineColor = lineColors[lines.index(points)]
        lineThickness = lineThicknesses[lines.index(points)]
        if len(points) >= 2:
            pygame.draw.lines(screen, lineColor, False, points, lineThickness)

    pygame.display.flip()