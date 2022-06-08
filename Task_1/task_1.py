def input_data(input_text):
    result = input(input_text)
    try:
        result = float(result)
    except:
        # Avoid multiply of incorrect data message
        if 'Incorrect data submitted. ' not in input_text:
            input_text = 'Incorrect data submitted. ' + input_text
        result = input_data(input_text)
    return result


def triangle_exist(a,b,c):
    # Check existence
    if (a + b) > c and (b + c) > a and (c + a) > b:
        result = 'Triangle exist - '
        # Check if equilateral
        if a == b == c:
            result += 'equilateral'
        # Check if isosceles
        elif a == b or a == c:
            result += 'isosceles'
        # Check if rectangular    
        elif a**2 == (b**2 + c**2) or b**2 == (a**2+ c**2) or c**2 == (a**2 + b**2):
            result += 'rectangular'
        # Run out of options versatile
        else:
             result += 'versatile'
    else:
        result = 'Triangle not exists'
    return result


def prepare_text(text):
    return input_data('Please input {0} triangle side lenth: '.format(text))


if __name__ == "__main__":
    a = prepare_text('first')
    b = prepare_text('second')
    c = prepare_text('third')
    print(triangle_exist(a,b,c))