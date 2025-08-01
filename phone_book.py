def main():
    n = int(input())
    contacts = {}
    for _ in range(n):
        parts = input().split()
        cmd = parts[0]
        if cmd == "add":
            number = int(parts[1])
            name = parts[2]
            contacts[number] = name
        elif cmd == "del":
            number = int(parts[1])
            contacts.pop(number, None)
        elif cmd == "find":
            number = int(parts[1])
            print(contacts.get(number, "not found"))

if __name__ == "__main__":
    main()
