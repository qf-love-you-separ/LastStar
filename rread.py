from PIL import Image
import rarfile
from io import BytesIO

def getRe(path):
    file = rarfile.RarFile(".\\assets\\" + path)
    namelist = file.namelist()
    list = []
    p = 0
    for i in namelist:
        with file.open(i) as f:
            p += 1
            c = Image.open(BytesIO(f.read()))
            c = c.resize((int(c.size[0]/2), int(c.size[1]/2)))
            list.append([c.tobytes(), c.size, "RGB"])
            # print(f"loaded: {round(p / len(namelist), 4) * 100}%")
    return list

if __name__ == "__main__":
    print(getRe("images\\trees\\tree1\\tree1.rar"))