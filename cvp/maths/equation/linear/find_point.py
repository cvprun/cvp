# -*- coding: utf-8 -*-


def find_x_given_y_on_line(line_x1, line_y1, line_x2, line_y2, y3):
    """
    Compute the x-value (`x3`) on a line for a given y-value (`y3`).
    """

    if line_x1 == line_x2 and line_y1 == line_y2:
        raise ValueError("The two points are identical. Not a valid line.")

    if line_x1 == line_x2:
        assert line_y1 != line_y2
        return line_x1

    if line_y1 == line_y2:
        assert line_x1 != line_x2
        if line_y1 != y3:
            raise ValueError("The given y-value does not lie on the horizontal line")
        else:
            raise ValueError("Infinite x-values on horizontal line.")

    assert line_x1 != line_x2
    assert line_y1 != line_y2

    slope = (line_y2 - line_y1) / (line_x2 - line_x1)
    return line_x1 + (y3 - line_y1) / slope
