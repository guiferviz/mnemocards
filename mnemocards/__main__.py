
from mnemocards import greet
from mnemocards._argument_parser import parse_args


def main():
    args = parse_args()

    if args.command == "generate":
        generate(args)
    elif args.command == "import":
        print("Import!!")
    elif args.command == "push":
        print("Push!!")
    elif args.command == "clone":
        print("Clone!!")
    elif args.command == "gists":
        print("Gists!!")
    elif args.command == "clean":
        print("Clean!!")
    elif args.command == "hi":
        greet()


if __name__ == "__main__":
    main()

