import json
from PIL import Image
from cuboid import Cuboid

class Objson:
    def __init__(self, obj_path, mtl_path):
        self.obj_path = obj_path
        self.mtl_path = mtl_path

        with open(obj_path) as f:
            self.obj = f.readlines()
        	
        # Extract verticies and face groups
        self.vertices = self.extract_vertices()
        self.raw_objects = self.extract_objects()

        # Creates cuboids from the raw objects
        self.cuboids = self.create_cuboids()
    
    def create_cuboids(self, vertices=None, raw_objects=None):
        if vertices is None:
            vertices = self.vertices

        if raw_objects is None:
            raw_objects = self.raw_objects


        cuboids = []

        for o in raw_objects:
            faces = []
            for face in raw_objects[o]:
                ## Splits a face into its 4 vertice indexes
                face_vertice_indexes = [int(x.split("/")[0]) - 1 for x in face]
                
                ## Converts the indexes into coordinates
                face_vertices = [vertices[x] for x in face_vertice_indexes]

                faces.append(face_vertices)

            cuboids.append(Cuboid(faces, o))
                
        return cuboids

    def extract_vertices(self, obj=None):
        if obj is None:
            obj = self.obj
        
        return [list(map(float, x.strip().split()[1:])) for x in obj if x.split()[0] == "v"]

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
                objects[current_object].append(x_split[1:])
        
        return objects
    
    def convert(self, json_path, texture_path):
        # Initialize JSON and
        with open("templates/geo.json") as f:
            self.json = json.load(f)
        self.texture = Image.new('RGB', (16, 16), color = 'red')
        
        self.json["minecraft:geometry"][0]["bones"][0]["cubes"] = [c.return_json() for c in self.cuboids]

        ## Save Files
        self.__save(json_path, texture_path)
    
    def __save(self, json_path, texture_path):
        with open(json_path, "w+") as f:
            json.dump(self.json, f, indent=4)
        self.texture.save(texture_path)