from parser import parser

def main():
    print("Parser & SDT")
    print("Escribe 'exit' para salir.\n")
    while True:
        try:
            data = input(">> ")
        except EOFError:
            break
        if data.lower() == "exit":
            break
        if not data.strip():
            continue
        parser.parse(data)

if __name__ == "__main__":
    main()
