import math

OFFSET = 1000
PRODUCT_COUNT = 350


def count_correlation(sessions):
    matrix = []
    products = [0] * PRODUCT_COUNT

    products_count = 0
    sessions_count = 0

    correlation = 0

    for i in range(0, PRODUCT_COUNT):
        new = []
        for j in range(0, PRODUCT_COUNT):
            new.append(0)
        matrix.append(new)

    first_product = sessions[0]['product_id']
    products[first_product - OFFSET] += 1

    for count in range(1, len(sessions)):

        curr_product = sessions[count]['product_id']
        prev_product = sessions[count - 1]['product_id']

        curr_user = sessions[count]['user_id']
        prev_user = sessions[count]['user_id']

        if curr_product:
            products[curr_product - OFFSET] += 1
            products_count += 1

            if prev_product:
                if curr_user == prev_user:
                    sessions_count += 1
                    matrix[prev_product - OFFSET][curr_product - OFFSET] += 1

    for row in range(0, PRODUCT_COUNT):
        for col in range(0, PRODUCT_COUNT):
            x_probability = products[row] / products_count
            y_probability = products[col] / products_count
            xy_probability = matrix[row][col] / sessions_count

            if x_probability and y_probability and xy_probability:
                correlation += xy_probability * math.log10(xy_probability / (x_probability * y_probability))

    return correlation
