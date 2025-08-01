def check_brackets(text):
    stack = []
    for i, char in enumerate(text):
        if char in '([{':
            stack.append((char, i + 1))
        elif char in ')]}':
            if not stack:
                return i + 1
            top, pos = stack.pop()
            if (top == '(' and char != ')') or \
               (top == '[' and char != ']') or \
               (top == '{' and char != '}'):
                return i + 1
    if stack:
        return stack[0][1]
    return "Success"


if __name__ == "__main__":
    text = input()
    print(check_brackets(text))
