import json

def readLevel(level):
    return json.load(open(f".\\assets\\levels\\level{level}.json", "r"))

if __name__ == "__main__":
    print(readLevel(1))