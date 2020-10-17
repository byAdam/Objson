import json
from PIL import Image

class Objson:
    def __init__(self, obj_path, mtl_path):
        self.obj_path = obj_path
        self.mtl_path = mtl_path

        with open(obj_path) as f:
            self.obj = f.readlines()
        	
        # Extract verticies and face groups
        self.vertices = self.extract_vertices()
        self.raw_objects = self.extract_objects()

    def extract_vertices(self, obj=None):
        if obj is None:
            obj = self.obj
        
        return [x.strip() for x in obj if x.split()[0] == "v"]

    def extract_objects(self, obj=None):
        if obj is None:
            obj = self.obj

        objects = {}
        current_object = ""

        for x in obj:
            x_split = x.strip().split()

            ## If Object
            if x_split[0] == "o":
                current_object = x_split[1]
                objects[current_object] = []

            ## If Faces
            if x_split[0] == "f":
                objects[current_object].append([x_split[1:]])
        
        return object
    
    def convert(self, json_path, texture_path):
        # Initialize JSON and
        self.json = {}
        self.texture = Image.new('RGB', (16, 16), color = 'red')

        print(self.vertices)
        print(self.raw_objects)

        ## Save Files
        self.__save(json_path, texture_path)
    
    def __save(self, json_path, texture_path):
        with open(json_path, "w+") as f:
            json.dump(self.json, f)
        self.texture.save(texture_path)