from tkinter import Tk, Button, Label, Entry, END, Listbox, Canvas
from tkinter import messagebox
from func import *


WIN_WIDTH = 1400
WIN_HEIGHT = 800

CV_WIDE = 1100
CV_HEIGHT = 800

TASK = "На плоскости дано множество точек. Найти такой треугольник с вершинами в этих точках, у которого угол, образованный прямой, соединяющей точку пересечения высот и начало координат, и осью ординат максимален."


def init_input_win():
    '''
        Функция для создания окна для ввода или изменения координат точки
    '''
    dot_win = Tk()
    dot_win.title("Точка")
    dot_win['bg'] = "orange"
    dot_win.geometry("270x200")
    dot_win.resizable(False, False)

    dot_x_label = Label(dot_win, text = "X: ", bg = "orange", font="-family {Consolas} -size 14")
    dot_x_label.place(x = 3, y = 30)
    dot_x = Entry(dot_win, font="-family {Consolas} -size 14")
    dot_x.focus()
    dot_x.place(x = 27, y = 30)

    dot_y_label = Label(dot_win, text = "Y: ", bg = "orange", font="-family {Consolas} -size 14")
    dot_y_label.place(x = 3, y = 70)
    dot_y = Entry(dot_win, font="-family {Consolas} -size 14")
    dot_y.place(x = 27, y = 70)

    return dot_win, dot_x, dot_y


def del_dot(dots_block, dots_list):
    '''
        Функция для удаления точки их выбранного множества
    '''
    try:
        place = dots_block.curselection()[0]
        dots_list.pop(place)

        dots_block.delete(0, END)

        for i in range(len(dots_list)):
            dot_str = "%d) (%-3.1f,%-3.1f)" %(i + 1, float(dots_list[i][0]), float(dots_list[i][1]))
            dots_list[i][2] = i + 1
            dots_block.insert(END, dot_str)
    except:
        messagebox.showerror("Ошибка", "Не выбрана точка для удаления")


def del_all_dots(dots_block, dots_list):
    '''
        Функция для удаления всех точек текущего множества
    '''
    if (len(dots_list) != 0):
        dots_block.delete(0, END)
        dots_list.clear()
    else:
        messagebox.showerror("Ошибка", "Нечего удалять")


def change_dot(dots_block, dots_list):
    '''
        Функция для изменения координат точки выбранного множества
    '''
    try:
        place = dots_block.curselection()[0]
    except:
        messagebox.showerror("Ошибка", "Не выбрана точка для изменения")
        return

    dot_win, dot_x, dot_y = init_input_win()

    add_but = Button(dot_win, text = "Изменить", font="-family {Consolas} -size 14", command = lambda: read_dot(dots_block, dots_list, place, dot_x.get(), dot_y.get()))
    add_but.place(x = 70, y = 120)

    dot_win.mainloop()


def read_dot(dots_block, dots_list, place, dot_x, dot_y):
    '''
        Функция для чтения координат точки, их обработки и добавления в множество
    '''
    try:
        coords_dot = []

        coords_dot.append(float(dot_x))
        coords_dot.append(float(dot_y))

        if (place != END): # если нужно изменить точку
            dots_block.delete(place)
            dots_list.pop(place)
            coords_dot.append(place + 1)
            dots_list.insert(place, coords_dot)
        else: # если нужно добавить новую точку
            place = len(dots_list)
            coords_dot.append(place + 1)
            dots_list.append(coords_dot)

        dot_str = "%d) (%-3.1f,%-3.1f)" %(place + 1, float(dot_x), float(dot_y))
        dots_block.insert(place, dot_str)

        # print(dots_list)
    except:
        messagebox.showerror("Ошибка", "Неверно введены координаты точки")


def add_dot(dots_block, dots_list):
    '''
        Функция для добавления точки в множество
    '''
    dot_win, dot_x, dot_y = init_input_win()

    add_but = Button(dot_win, text = "Добавить", font="-family {Consolas} -size 14", command = lambda: read_dot(dots_block, dots_list,END, dot_x.get(), dot_y.get()))
    add_but.place(x = 70, y = 120)

    dot_win.mainloop()


def print_result(rem_data, angle):
    '''
        Функция для вывода результатов вычисления (максимального угла), а также обозначения всех линий на холсте
    '''

    if (angle == 0):
        messagebox.showinfo("Угол", "Нельзя вычислить угол, так как треугольник не может существовать")
        return

    res_win = Tk()
    res_win.title("Результаты")
    res_win.geometry("850x400")
    res_win.resizable(False, False)

    res_label = Label(res_win, text = "Результаты", font="-family {Consolas} -size 14", fg = "black")
    res_label.place(x = 400, y = 15)

    triangle1_label = Label(res_win, text = "Треугольник", font="-family {Consolas} -size 14", fg = TRIANGLE_COLOR)
    triangle1_label.place(x = 100, y = 50)

    biseks1_label = Label(res_win, text = "Высоты треугольника", font="-family {Consolas} -size 14", fg = HEGHT_COLOR)
    biseks1_label.place(x = 100, y = 75)

    intersec1_label = Label(res_win, text = "Точка пересечения высот - [%3.1f;%3.1f]" %(rem_data[0][0], rem_data[0][1]) , font="-family {Consolas} -size 14", fg = "black")
    intersec1_label.place(x = 100, y = 100)

    result_line_label = Label(res_win, text = "Линия, соединяющая точку пересечения\n     высот и  начало координат", font="-family {Consolas} -size 14", fg = RESULT_LINE_COLOR)
    result_line_label.place(x = 100, y = 150)

    axis_label = Label(res_win, text = "Оси координат (декартовые)", font="-family {Consolas} -size 14", fg = AXIS_COLOR)
    axis_label.place(x = 100, y = 200)


    angle_label = Label(res_win, text = "ОТВЕТ: угол между линией, соединяющей точку пересечения высот \n и начало координат, и осью OY равен   %3.2f   градусов" %(angle), font="-family {Consolas} -size 14", fg = "black")
    angle_label.place(x = 50, y = 250)

    res_win.mainloop()


def build_triangle(rem_data, x_min, y_min, k, triangle_color, point_name_color):
    '''
        Функция для отрисовки треугольника
    '''
    x1, y1 = rem_data[1][0], rem_data[1][1]
    x2, y2 = rem_data[2][0], rem_data[2][1]
    x3, y3 = rem_data[3][0], rem_data[3][1]

    x2_h, y2_h = intersection_point(rem_data[0], rem_data[2], rem_data[1], rem_data[3])
    x1_h, y1_h = intersection_point(rem_data[0], rem_data[1], rem_data[2], rem_data[3])
    x3_h, y3_h = intersection_point(rem_data[0], rem_data[3], rem_data[1], rem_data[2])

    x1_trans, y1_trans = translate_point(x1, y1, x_min, y_min, k)
    x2_trans, y2_trans = translate_point(x2, y2, x_min, y_min, k)
    x3_trans, y3_trans = translate_point(x3, y3, x_min, y_min, k)

    x1_h, y1_h = translate_point(x1_h, y1_h, x_min, y_min, k)
    x2_h, y2_h = translate_point(x2_h, y2_h, x_min, y_min, k)
    x3_h, y3_h = translate_point(x3_h, y3_h, x_min, y_min, k)

    heights_dict = {(x1_h, y1_h): [x1_trans, y1_trans], (x2_h, y2_h): [x2_trans, y2_trans], (x3_h, y3_h): [x3_trans, y3_trans]}

    canvas_win.create_line(x1_trans, -y1_trans + CV_HEIGHT, x2_trans, -y2_trans + CV_HEIGHT, width = 4, fill = "black")
    canvas_win.create_line(x2_trans, -y2_trans + CV_HEIGHT, x3_trans, -y3_trans + CV_HEIGHT, width = 4, fill = "black")
    canvas_win.create_line(x1_trans, -y1_trans + CV_HEIGHT, x3_trans, -y3_trans + CV_HEIGHT, width = 4, fill = "black")

    if in_triangle(rem_data[0], rem_data[1], rem_data[2], rem_data[3]) == -1:
        for point in ((x1_h, y1_h), (x2_h, y2_h), (x3_h, y3_h)):
            if in_triangle(point, [x1_trans, y1_trans], [x2_trans, y2_trans], [x3_trans, y3_trans]) != -1:
                main_point = heights_dict[point]
        for point in ((x1_h, y1_h), (x2_h, y2_h), (x3_h, y3_h)):
            if in_triangle(point, [x1_trans, y1_trans], [x2_trans, y2_trans], [x3_trans, y3_trans]) == -1:
                canvas_win.create_line(point[0], -point[1] + CV_HEIGHT, main_point[0], -main_point[1] + CV_HEIGHT, width = 4, fill = "orange")

    canvas_win.create_oval(x1_trans - POINT_RAD, -(y1_trans - POINT_RAD) + CV_HEIGHT, x1_trans + POINT_RAD, -(y1_trans + POINT_RAD) + CV_HEIGHT, width = 1, outline = POINT_COLOR, fill = POINT_COLOR)
    canvas_win.create_oval(x2_trans - POINT_RAD, -(y2_trans - POINT_RAD) + CV_HEIGHT, x2_trans + POINT_RAD, -(y2_trans + POINT_RAD) + CV_HEIGHT, width = 1, outline = POINT_COLOR, fill = POINT_COLOR)
    canvas_win.create_oval(x3_trans - POINT_RAD, -(y3_trans - POINT_RAD) + CV_HEIGHT, x3_trans + POINT_RAD, -(y3_trans + POINT_RAD) + CV_HEIGHT, width = 1, outline = POINT_COLOR, fill = POINT_COLOR)

    name_point(x1, y1, 1, x1_trans, y1_trans, x2_trans, y2_trans, x3_trans, y3_trans, point_name_color)
    name_point(x2, y2, 2, x2_trans, y2_trans, x1_trans, y1_trans, x3_trans, y3_trans, point_name_color)
    name_point(x3, y3, 3, x3_trans, y3_trans, x2_trans, y2_trans, x1_trans, y1_trans, point_name_color)


def build_height(rem_data, x_min, y_min, k, line_color):
    '''
        Функция для отрисовки высот треугольника и точки их пересечения
    '''
    x0, y0 = rem_data[0][0], rem_data[0][1]
    x1, y1 = rem_data[1][0], rem_data[1][1]
    x2, y2 = rem_data[2][0], rem_data[2][1]
    x3, y3 = rem_data[3][0], rem_data[3][1]

    x2_h, y2_h = intersection_point(rem_data[0], rem_data[2], rem_data[1], rem_data[3])
    x1_h, y1_h = intersection_point(rem_data[0], rem_data[1], rem_data[2], rem_data[3])
    x3_h, y3_h = intersection_point(rem_data[0], rem_data[3], rem_data[1], rem_data[2])

    x1_trans, y1_trans = translate_point(x1, y1, x_min, y_min, k)
    x2_trans, y2_trans = translate_point(x2, y2, x_min, y_min, k)
    x3_trans, y3_trans = translate_point(x3, y3, x_min, y_min, k)

    x1_h, y1_h = translate_point(x1_h, y1_h, x_min, y_min, k)
    x2_h, y2_h = translate_point(x2_h, y2_h, x_min, y_min, k)
    x3_h, y3_h = translate_point(x3_h, y3_h, x_min, y_min, k)

    x0, y0 = translate_point(x0, y0, x_min, y_min, k)

    heights_dict = {(x1_h, y1_h): [x1_trans, y1_trans], 
                    (x2_h, y2_h): [x2_trans, y2_trans],
                    (x3_h, y3_h): [x3_trans, y3_trans]
                    }

    print("Первая точка треугольника до перевода ", [x1, y1], "\n", "Первая точка после перевода ", [x1_trans, y1_trans], "\n",
        "Вторая точка треугольника до перевода ", [x2, y2], "\n", "Вторая точка после перевода ", [x2_trans, y2_trans], "\n",
        "Третья точка треугольника до перевода ", [x3, y3], "\n", "Третья точка после перевода ", [x3_trans, y3_trans], "\n")

    canvas_win.create_line(x1_trans, -y1_trans + CV_HEIGHT, x1_h, -y1_h + CV_HEIGHT, width = 4, fill = line_color)
    canvas_win.create_line(x2_trans, -y2_trans + CV_HEIGHT, x2_h, -y2_h + CV_HEIGHT, width = 4, fill = line_color)
    canvas_win.create_line(x3_trans, -y3_trans + CV_HEIGHT, x3_h, -y3_h + CV_HEIGHT, width = 4, fill = line_color)

    if in_triangle(rem_data[0], rem_data[1], rem_data[2], rem_data[3]) == -1:
        for i in [(x1_h, y1_h), (x2_h, y2_h), (x3_h, y3_h)]:
            if in_triangle(i, [x1_trans, y1_trans], [x2_trans, y2_trans], [x3_trans, y3_trans]) == -1:
                canvas_win.create_line(i[0], -i[1] + CV_HEIGHT, x0, -y0 + CV_HEIGHT, width=4, fill = "red")
            else:
                # print(heights_dict[i][0], -heights_dict[i][1])
                canvas_win.create_line(heights_dict[i][0], -heights_dict[i][1] + CV_HEIGHT, x0, -y0 + CV_HEIGHT, width = 4, fill = "red")

    canvas_win.create_oval(x0 - POINT_RAD, -(y0 - POINT_RAD) + CV_HEIGHT, x0 + POINT_RAD, -(y0 + POINT_RAD) + CV_HEIGHT, width = 1, outline = "red", fill = "red")


def draw_axises(x_min, y_min, k, color):
    '''
        Функция для отрисовки осей координат
    '''
    x_axis_x1, x_axis_y1 = translate_point(CV_WIDE, 0, x_min, y_min, k)
    x_axis_x2, x_axis_y2 = translate_point(-CV_WIDE, 0, x_min, y_min, k)

    y_axis_x1, y_axis_y1 = translate_point(0 , CV_HEIGHT, x_min, y_min, k)
    y_axis_x2, y_axis_y2 = translate_point(0, -CV_HEIGHT, x_min, y_min, k)

    # print(x_axis_x1, x_axis_x2, y_axis_y1, y_axis_y2)

    # Coord lines
    canvas_win.create_line(-CV_WIDE, -x_axis_y1 + CV_HEIGHT, CV_WIDE, -x_axis_y2 + CV_HEIGHT, width = 4, fill = color)
    canvas_win.create_line(y_axis_x1, -CV_HEIGHT, y_axis_x2, CV_HEIGHT, width = 4, fill = color)


def draw_result_line(rem_data, x_min, y_min, k, color):
    '''
        Функция для отрисовки линии, соединяющей точку пересечения высот треугольника и начало координат
    '''
    x1_c, y1_c = translate_point(rem_data[0][0], rem_data[0][1], x_min, y_min, k)

    x_axis, y_axis = 0, 0
    x_axis, y_axis = translate_point(x_axis, y_axis, x_min, y_min, k)


    canvas_win.create_line(x1_c, -y1_c + CV_HEIGHT, x_axis, -y_axis + CV_HEIGHT, width = 4, fill = color) # axis and one of centers

    canvas_win.create_oval(x1_c - POINT_RAD, -(y1_c - POINT_RAD) + CV_HEIGHT, x1_c + POINT_RAD, -(y1_c + POINT_RAD) + CV_HEIGHT, width = 1, outline = "red", fill = "red")


def solution(dots1_list):
    """
        Функция, на которой держится все
    """
    canvas_win.delete("all")
    rem_data, angle = max_angle_triangle(dots1_list)
    if angle != 0:
        # print(rem_data)
        draw_result(rem_data)
    print_result(rem_data, angle)


def draw_result(rem_data):
    '''
        Функция для вызова отрисовщиков всех необходимых объектов
    '''
    k, x_min, y_min = find_scale(rem_data)

    # Оси
    draw_axises(x_min, y_min, k, AXIS_COLOR)

     # Стороны трегуольника
    build_triangle(rem_data, x_min, y_min, k, TRIANGLE_COLOR, POINT_NAME_COLOR)
    
    # Высоты
    build_height(rem_data, x_min, y_min, k, HEGHT_COLOR)

    # Прямая из заданя
    draw_result_line(rem_data, x_min, y_min, k, RESULT_LINE_COLOR)


def name_point(x1, y1, num, x1_place, y1_place, x2_place, y2_place, x3_place, y3_place, color):
    '''
        Функция для вычисления нужного расположения точки и ее постановка на холст
    '''

    x_min = min(x1_place, x2_place, x3_place)
    x_max = max(x1_place, x2_place, x3_place)
    y_min = min(y1_place, y2_place, y3_place)
    y_max = max(y1_place, y2_place, y3_place)

    move_x = 0
    move_y = 0

    if (x1_place == x_min):
        move_x -= 15
    if (x1_place == x_max):
        move_x += 15
    if (y1_place == y_min):
        move_y -= 15
    if (y1_place == y_max):
        move_y += 15

    if (move_x == 0) and (move_y == 0):
        if (x1_place > x2_place):
            move_x -= 20
        else:
            move_x += 20

        if (y1_place > y2_place):
            move_y -= 20
        else:
            move_y += 20


    canvas_win.create_text(x1_place + move_x, 
                           -(y1_place + move_y) + CV_HEIGHT, 
                           text = "(%d) [%.1f;%.1f]" %(num, x1, y1), 
                           font="-family {Consolas} -size 11", 
                           fill = color)



if __name__ == "__main__":
    '''
        Тело программы, организующее работу главного окна
    '''

    dots1_list = []

    win = Tk()
    win['bg'] = 'orange'
    win.geometry("%dx%d" %(WIN_WIDTH, WIN_HEIGHT))
    win.title("Лабораторная работа #1 (Тевс В.М. ИУ7-42Б)")
    win.resizable(False, False)

    canvas_win = Canvas(win, width = CV_WIDE, 
                        height = CV_HEIGHT, 
                        bg = "#fff3e6")
    canvas_win.place(x = 300, y = 0)

    # Множество точек 1
    dots1_label = Label(text = "Множество точек 1", 
                        bg = 'orange', 
                        font="-family {Consolas} -size 18")
    dots1_label.place(x = 30, y = 10)

    dots1_block = Listbox(bg = "#fff3e6")
    dots1_block.configure(height = 15, width = 25)
    dots1_block.configure(font="-family {Consolas} -size 14")
    dots1_block.place(x = 10, y = 50)

    add1 = Button(text = "Добавить",
                    width = 9, 
                    height = 2,  
                    font="-family {Consolas} -size 14", 
                    command = lambda: add_dot(dots1_block, dots1_list))
    add1.place(x = 10, y = 430)

    del1 = Button(text = "Удалить", 
                  width = 9, 
                  height = 2, 
                  font="-family {Consolas} -size 14", 
                  command = lambda: del_dot(dots1_block, dots1_list))
    del1.place(x = 160, y = 430)

    chg1 = Button(text = "Изменить", 
                  width = 9, 
                  height = 2, 
                  font="-family {Consolas} -size 14", 
                  command = lambda: change_dot(dots1_block, dots1_list))
    chg1.place(x = 10, y = 500)

    del_all1 = Button(text = "Очистить\nвсё", 
                      width = 9, 
                      height = 2, 
                      font="-family {Consolas} -size 14", 
                      command = lambda: del_all_dots(dots1_block, dots1_list))
    del_all1.place(x = 160, y = 500)

    canvas_win.delete("all")
    solve = Button(text = "Решить задачу", 
                   width = 23, 
                   height = 2, 
                   font="-family {Consolas} -size 14", 
                   command = lambda: solution(dots1_list))
    solve.place(x = 10, y = 600)

    task = Button(text = "Вывести условие задачи", 
                  width = 23, 
                  height = 2, 
                  font="-family {Consolas} -size 14", 
                  command = lambda: messagebox.showinfo("Задание", TASK))
    task.place(x = 10, y = 700)

    win.mainloop()
