def get_name(name):
    return name.upper()


def calculate_marks(m1, m2, m3):
    total = m1 + m2 + m3
    average = total / 3
    return total, average


def check_result(average):
    if average >= 60:
        return "Pass"
    else:
        return "Better luck next time!"


def fibo(n):
    series = []
    a = 0
    b = 1

    for i in range(n):
        series.append(a)
        a, b = b, a + b

    return series