from parser import parser

def main():
    print("Parser & SDT\nType 'exit' to quit.")
    while True:
        data = input(">> ")
        if data.lower() == 'exit':
            break
        if not data.strip():
            continue
        parser.parse(data)

if __name__ == "__main__":
    main()
