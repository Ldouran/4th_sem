from math import sqrt, degrees, atan2


WIN_WIDTH = 1400
WIN_HEIGHT = 800

CV_WIDE = 1100
CV_HEIGHT = 800

POINT_RAD = 3.5

TRIANGLE_COLOR = "green"
HEGHT_COLOR = "#1e4169"
POINT_NAME_COLOR = "black"
POINT_COLOR = "red"
RESULT_LINE_COLOR = "#9311d9"
AXIS_COLOR = "darkgray"

PLACE_TO_DRAW = 0.8
INDENT_WIDTH = 0.1

TASK = "На плоскости дано множество точек. Найти такой треугольник с вершинами в этих точках, у которого угол, образованный прямой, соединяющей точку пересечения высот и начало координат, и осью ординат максимален."


def find_scale(rem_data):
    '''
        Функция для нахождения коэффициента масштабирования (используя все точки полотна)
    '''
    print(rem_data)
    x_min = rem_data[0][0]
    y_min = rem_data[0][1]
    x_max = rem_data[0][0]
    y_max = rem_data[0][1]

    for point in rem_data:
        if (point[0] < x_min):
            x_min = point[0]
        if (point[1] < y_min):
            y_min = point[1]
        if (point[0] > x_max):
            x_max = point[0]
        if (point[1] > y_max):
            y_max = point[1]

    if y_min > 0:
        y_min = -1
    if x_min > 0:
        x_min = -1
    if x_max < 0:
        x_max = 1
    if y_max < 0:
        y_max = 1

    k_x = (PLACE_TO_DRAW * CV_WIDE) / (x_max - x_min)
    k_y = (PLACE_TO_DRAW * CV_HEIGHT) / (y_max - y_min)

    return min(k_x, k_y), x_min, y_min


def translate_point(x, y, x_min, y_min, k):
    '''
        Функция для перевода точки в нужные координаты (для масштабирования)
    '''
    x = INDENT_WIDTH * CV_WIDE + (x - x_min) * k
    y = INDENT_WIDTH * CV_HEIGHT + (y - y_min) * k

    return x, y


def line_coefficient(p1, p2):
    """
        Функция для нахождения коэффициента прямой по координатам
    """
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    if x2 != x1:
        k = (y2 - y1) / (x2 - x1)
    else:
        k = 0
    b = y1 - x1 * k
    # print("Прямая")
    # print(k, b, p1, p2)
    return k, b


def height_equation(ph, p1, p2):
    # kv = -1 / k (the coefficient of the straight line on which the height falls)
    """
        Функция для нахождения коэффициентов высоты в треугольнике
    """

    kv, b = line_coefficient(p1, p2)
    # print("Высота")
    # print(kv, b, p1, p2)
    if kv != 0:
        kv = -1 / kv

    b = ph[1] - ph[0] * kv

    return kv, b


def heights_intersection_point(p1, p2, p3):
    """
        Функция для нахождения точки пересечения высот в треугольнике
    """
    flag = 1
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x3, y3 = p3[0], p3[1]

    k1, b1 = line_coefficient(p1, p2)
    k2, b2 = line_coefficient(p2, p3)
    k3, b3 = line_coefficient(p1, p3)

    kv, bv = height_equation([0, 0], p2, p3)
    kv2, bv2 = height_equation([0, 0], p1, p3)
    kv3, bv3 = height_equation([0, 0], p1, p2)
    # x0 = 1
    # y0 = 10
    if k1 == k2:
        x0, y0 = p2[0], p2[1]
    elif k1 == k3:
        x0, y0 = p1[0], p1[1]
    elif k2 == k3:
        x0, y0 = p3[0], p3[1]
    else:
        flag = 0
        x0 = (y3 - y2 + kv2 * x2 - kv3 * x3) / (kv2 - kv3)
        y0 = y2 + kv2 * x0 - kv2 * x2
        # print(p1, p2, p3, x0, y0)
    # print(p1, p2, p3, [x0, y0], kv2, kv3)
    # print("x0 = %f, y0 = %f" % (x0, y0))

    return x0, y0, flag


def distance(p1, p2):
    """
        Функция для нахождения длины между двумя точками
    """

    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def check_triangle(p1, p2, p3):
    """
        Функция для проверки существования треугольника(Если одна сторона больше меньше чем сумма двух других)
    """
    a = distance(p1, p2)
    b = distance(p2, p3)
    c = distance(p1, p3)

    if (a + b > c) and (a + c > b) and (b + c > a):
        return 1
    else:
        return 0


def intersection_point(p1, p2, p3, p4):
    """
        Функция для нахождения точки пересечения между высотой и прямой на которую она опирается
    """
    flag = p1[2]
    p1 = [p1[0], p1[1]]
    if p1[0] != p2[0] and p1[1] != p2[1]:
        k1, b1 = line_coefficient(p1, p2)
    else:
        k1, b1 = height_equation(p1, p3, p4)
    k2, b2 = line_coefficient(p3, p4)
    if k1 - k2 != 0:
        x = (b2 - b1) / (k1 - k2)
        y = k1 * x + b1
    else:
        if flag == 1:
            x, y = p1[0], p1[1]
        else:
            x, y = p2[0], p3[1]
    '''
    print("Точка пересечения высот ", p1, "\n", "Точка из которой исходит высота ", p2, "\n",
          "Первая вершина прямой на которую падает высота ", p3, "\n",
          "Вторая вершина прямой на которую падает высота ", p4, "\n",
          "Коффициент высоты = ", k1, "\n", "В высоты = ", b1, "\n",
          "Коффициент прямой = ", k2, "\n", "В прямой = ", b2, "\n",
          "Точка пересечения высоты и прямой ", [x, y])
    print()
    '''
    return x, y, 


def in_triangle(ph, p1, p2, p3):
    """
        Функция для проверки принадлежности точки к треугольнику
    """
    # print(ph)
    x0, y0 = round(ph[0], 5), round(ph[1], 4)
    x1, y1 = round(p1[0], 5), round(p1[1], 4)
    x2, y2 = round(p2[0], 5), round(p2[1], 4)
    x3, y3 = round(p3[0], 5), round(p3[1], 4)
    rs = -1

    s = round(1/2 * abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)), 4)
    s1 = round(1/2 * abs((x2 - x1) * (y0 - y1) - (x0 - x1) * (y2 - y1)), 4)
    s2 = round(1/2 * abs((x0 - x1) * (y3 - y1) - (x3 - x1) * (y0 - y1)), 4)
    s3 = round(1/2 * abs((x2 - x0) * (y3 - y0) - (x3 - x0) * (y2 - y0)), 4)

    if s == s1 + s2 + s3:
        rs = 1
        if s1 == 0 or s2 == 0 or s3 == 0:
            rs = 0
    print("--------------------------------------")
    print("Точка для проверки ", ph, "\n", "1 точка треугольника ", p1, "\n", "2 точка треугольника ", p2, 
        "\n", "3 точка треугольника ", p3, "\n", "статус ", rs, "\n", "Общая площадь ", s, "\n",
        "Площадь 1 треугольника", s1, "\n", "Площадь второго треугольника", s2, "\n", "Площадь третьего треугольника", s3, "\n", "Сумма площадей", s1+s2+s3, "\n")
    print("--------------------------------------")
    return rs


def near(p, lp):
    """
        Функция для вычисления близжайшей точки к заданной точке
    """
    ans = lp[0]
    if distance(p, lp[0]) > distance(p, lp[1]):
        ans = lp[1]
    return ans


def max_angle_triangle(points_def):
    """
        Функция для нахождения нужного максимального угла среди всех возможнных треугольников
    """
    max_angle = 0
    max_triangle_def = []
    angles = []
    triangles = []
    angle = 0
    for i in range(len(points_def)):
        for j in range(i + 1, len(points_def)):
            for k in range(j + 1, len(points_def)):
                # check if triangle can exist
                if check_triangle(points_def[i], points_def[j], points_def[k]):
                    # print(points_def)
                    # compute the intersection point of the heights
                    inter_point = heights_intersection_point(points_def[i], points_def[j], points_def[k])
                    # compute the angle between the height and the y-axis
                    # print(inter_point[1], inter_point[0])
                    angles.append(90 - degrees(atan2(inter_point[1], inter_point[0])))
                    triangles.append([points_def[i], points_def[j], points_def[k]])
                    # print(angles)
                    angle = angles[-1]
                    if angle > max_angle:
                        max_angle = angle
                        max_triangle_def = [inter_point, points_def[i], points_def[j], points_def[k]]
                # elif angle == 0:
                #    print(
                #        'Невозможно вычислить угол, потому что треугольник не может существовать')
    # print(points)
    # print(angles)
    # print(triangles)
    # print(max_angle)
    return max_triangle_def, max_angle
