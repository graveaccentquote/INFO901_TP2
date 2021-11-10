from src.test1 import main as test1

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("usage: {} image output".format(sys.argv[0]))
        sys.exit(1)
    test1(sys.argv[1], sys.argv[2])
