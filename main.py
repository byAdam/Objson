from objson import Objson
import sys

def main():
    args = sys.argv[1:]

    ## Pad args with None values up to 4
    args = [args[i] if i < len(args) else None for i in range(4)]

    obj_path = args[0]
    mtl_path = args[1]
    json_path = args[2]
    texture_path = args[3]

    if obj_path is None:
        obj_path = "input.obj"
    
    if json_path is None:
        json_path = "output.json"

    if texture_path is None:
        texture_path = "output.png"

    objson = Objson(obj_path, mtl_path)
    objson.convert(json_path, texture_path)


if __name__ == "__main__":
    main()