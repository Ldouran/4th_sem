from math import sqrt, degrees, atan2
import matplotlib.pyplot as plt


def line_coefficient(p1, p2):
    """
        Function for calculating the coefficient of a straight line (by coordinates)
    """
    x1, y1 = p1
    x2, y2 = p2

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
        Function for finding the coefficient of the straight height of a triangle
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
        Function for finding the intersection point of the triangle heights
    """
    flag = 1
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    k1, b1 = line_coefficient(p1, p2)
    k2, b2 = line_coefficient(p2, p3)
    k3, b3 = line_coefficient(p1, p3)

    kv, bv = height_equation([0, 0], p2, p3)
    kv2, bv2 = height_equation([0, 0], p1, p3)
    kv3, bv3 = height_equation([0, 0], p1, p2)
    # x0 = 1
    # y0 = 10
    if k1 == k2:
        x0, y0 = p2
    elif k1 == k3:
        x0, y0 = p1
    elif k2 == k3:
        x0, y0 = p3
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
        Function for calculating the length of a segment by coordinates
    """

    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def check_triangle(p1, p2, p3):
    """
        Function for checking the existence of a triangle (if one side is greater than the sum of its two sides)
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
        Function for finding the intersection point of the triangle height and line
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
            x = p1[0]
            y = p1[1]
        else:
            x = p2[0]
            y = p3[1]
    '''
    print("Точка пересечения высот ", p1, "\n", "Точка из которой исходит высота ", p2, "\n",
          "Первая вершина прямой на которую падает высота ", p3, "\n",
          "Вторая вершина прямой на которую падает высота ", p4, "\n",
          "Коффициент высоты = ", k1, "\n", "В высоты = ", b1, "\n",
          "Коффициент прямой = ", k2, "\n", "В прямой = ", b2, "\n",
          "Точка пересечения высоты и прямой ", [x, y])
    print()
    '''
    return x, y


def max_angle_triangle(points_def):
    max_angle = -1
    max_triangle_def = []
    angles = []
    triangles = []
    angle = 0
    for i in range(len(points_def)):
        for j in range(i + 1, len(points_def)):
            for k in range(j + 1, len(points_def)):
                # check if triangle can exist
                if check_triangle(points_def[i], points_def[j], points_def[k]):
                    # compute the intersection point of the heights
                    inter_point = heights_intersection_point(points_def[i], points_def[j], points_def[k])
                    # compute the angle between the height and the y-axis
                    # print(inter_point[1], inter_point[0])
                    angles.append(90 - degrees(atan2(inter_point[1], inter_point[0])))
                    triangles.append([points_def[i], points_def[j], points_def[k]])
                    angle = angles[-1]
                    if angle > max_angle:
                        max_angle = angle
                        max_triangle_def = [points_def[i], points_def[j], points_def[k]]
                elif angle == 0:
                    print(
                        'It is impossible to calculate the angle, so the points do not form a triangle that can exist')
    # print(points)
    # print(angles)
    # print(triangles)
    return max_triangle_def


def in_triangle(ph, p1, p2, p3):
    """
        Function for check if point in triangle or on the side
    """
    # print(ph)
    x0, y0 = ph
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    rs = -1

    s = 1/2 * abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
    s1 = round(1/2 * abs((x2 - x1) * (y0 - y1) - (x0 - x1) * (y2 - y1)), 10)
    s2 = round(1/2 * abs((x0 - x1) * (y3 - y1) - (x3 - x1) * (y0 - y1)), 10)
    s3 = round(1/2 * abs((x2 - x0) * (y3 - y0) - (x3 - x0) * (y2 - y0)), 10)

    if s == s1 + s2 + s3:
        rs = 1
        if 0 in [s1, s2, s3]:
            rs = 0
    if round(ph[0]) == round(4.215384615384617):
        print("Точка для проверки ", ph, "\n", "Первая точка треугольника ", p1, "\n",
              "Вторая точка треугольника ", p2, "\n",
              "Третья точка треугольника ", p3, "\n",
              "Общая площадь треугольника", s, "\n",
              "Площадь 012 = ", s1, "\n", "Площадь 013 = ", s2, "\n",
              "Площадь 023 = ", s3, "\n", "Нахождение точки ", rs, "\n",
              "Общая площадь по подсчетам ", s1 + s2 + s3)
        print()
    return rs


def near(p, lp):
    """
        Function for calculate nearest point for point
    """
    ans = lp[0]
    if distance(p, lp[0]) > distance(p, lp[1]):
        ans = lp[1]
    return ans


def draw_triangle(triangle):
    """
        black - triangle sides
        red - triangle heights
        blue - continuation of sides of triangle
        orange - continuation of heights
        green - straight line from (0, 0) to heights intersection point
    """
    # plot the vertices of a triangle
    plt.scatter([p[0] for p in triangle], [p[1] for p in triangle], color='blue')
    # plot the sides of a triangle
    plt.plot([triangle[0][0], triangle[1][0]], [triangle[0][1], triangle[1][1]], color='black')
    plt.plot([triangle[1][0], triangle[2][0]], [triangle[1][1], triangle[2][1]], color='black')
    plt.plot([triangle[0][0], triangle[2][0]], [triangle[0][1], triangle[2][1]], color='black')
    # calculate the intersection point of heights
    h_inter = heights_intersection_point(triangle[0], triangle[1], triangle[2])
    # calculate the intersection points of heights and sides of a triangle
    h1_inter = intersection_point(h_inter, triangle[0], triangle[1], triangle[2])
    h2_inter = intersection_point(h_inter, triangle[1], triangle[2], triangle[0])
    h3_inter = intersection_point(h_inter, triangle[2], triangle[0], triangle[1])
    point_dict = {h1_inter: [triangle[1], triangle[2]], h2_inter: [triangle[2], triangle[0]], h3_inter: [triangle[0], triangle[1]]}
    height_dict = {h1_inter: triangle[0], h2_inter: triangle[1], h3_inter: triangle[2]}
    # plot the heights
    # print(h1_inter, h2_inter, h3_inter, triangle)
    plt.plot([triangle[0][0], h1_inter[0]], [triangle[0][1], h1_inter[1]], color='red')
    plt.plot([triangle[1][0], h2_inter[0]], [triangle[1][1], h2_inter[1]], color='red')
    plt.plot([triangle[2][0], h3_inter[0]], [triangle[2][1], h3_inter[1]], color='red')
    h_inter = [h_inter[0], h_inter[1]]
    if in_triangle(h_inter, triangle[0], triangle[1], triangle[2]) == -1:
        for point in [h1_inter, h2_inter, h3_inter]:
            if in_triangle(point, triangle[0], triangle[1], triangle[2]) == -1:
                # print(triangle)
                near_point = near(point, point_dict[point])
                plt.plot([point[0], near_point[0]], [point[1], near_point[1]], color='blue')
                plt.plot([h_inter[0], point[0]], [h_inter[1], point[1]], color='orange')
            else:
                plt.plot([h_inter[0], height_dict[point][0]], [h_inter[1], height_dict[point][1]], color='orange')
    plt.plot([0, h_inter[0]], [0, h_inter[1]], color='green')

    plt.show()


points = [(1, 3), (10, 1), (4, 13)]
max_triangle = max_angle_triangle(points)
if max_triangle:
    # print(max_triangle)
    # print(max_triangle)
    draw_triangle(max_triangle)
