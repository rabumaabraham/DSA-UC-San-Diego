class StackWithMax:
    def __init__(self):
        self.stack = []
        self.max_stack = []

    def push(self, value):
        self.stack.append(value)
        if not self.max_stack or value >= self.max_stack[-1]:
            self.max_stack.append(value)

    def pop(self):
        if self.stack:
            if self.stack[-1] == self.max_stack[-1]:
                self.max_stack.pop()
            self.stack.pop()

    def max(self):
        return self.max_stack[-1] if self.max_stack else None

def main():
    stack = StackWithMax()
    for _ in range(int(input())):
        parts = input().split()
        if parts[0] == "push":
            stack.push(int(parts[1]))
        elif parts[0] == "pop":
            stack.pop()
        elif parts[0] == "max":
            print(stack.max())

if __name__ == "__main__":
    main()
