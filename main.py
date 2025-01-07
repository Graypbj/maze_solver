from graphics import Window, Point, Line

def main():
    win = Window(800, 600)
    point1 = Point(0, 0)
    point2 = Point(20, 20)
    new_line = Line(point1, point2)
    win.draw_line(new_line, "black")
    win.wait_for_close()

if __name__ == "__main__":
    main()
