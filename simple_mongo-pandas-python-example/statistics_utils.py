import statistics


def calculate_min(values, index):
    return min(values[index])


def calculate_max(values, index):
    return max(values[index])


def calculate_average(values, index):
    return statistics.mean(values[index])


def calculate_median(values, index):
    return statistics.median(values[index])
