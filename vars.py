def AcquisitionTimeStamp(x):
    return int(x)


def Matrix_helper(x):
    return int(x[0]), int(x[1]), float(x[2])


def Matrix(x):
    return [Matrix_helper(y.split(';')) for y in x[1: -1].split('][') if y]


variables = {'AcquisitionTimeStamp': AcquisitionTimeStamp, 'Matrix': Matrix}
