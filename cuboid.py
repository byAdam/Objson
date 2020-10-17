class Cuboid:
    def __init__(self, faces, name):
        self.faces = faces
        self.name = name
    
        self.sides = self.find_sides()
        self.origin = self.find_origin()

        self.dimensions = self.find_dimensions()
        self.rotation = [0, 0, 0]

    def return_json(self):
        return {"origin": self.origin, "size": self.dimensions, "uv": [0, 0], "pivot": self.origin}


    def find_origin(self, faces=None):
        if faces is None:
            faces = self.faces

        vertices = [x for f in faces for x in f]
        vertices_clean = []

        ## Remove duplicates
        for v in vertices:
            if v not in vertices_clean:
                vertices_clean.append(v)
        
        midpoint = []
        for i in range(3):
            midpoint.append(sum([v[i] for v in vertices_clean])/8)
        
        return midpoint

    def find_dimensions(self, sides=None):
        if sides is None:
            sides = self.sides

        dimensions = [0, 0, 0]

        for s in sides:
            axis = self.find_closest_axis(s[1])
            
            dimensions[axis] = s[0]

        return dimensions

    ## Finds the closest x, y, z (0, 1, 2) axis to a direction vector
    def find_closest_axis(self, v):
        return v.index(max(v))

    def find_sides(self, faces=None):
        if faces is None:
            faces = self.faces
        
        vectors = []
        
        ## Loop through each face, finding distance between connected vertices
        for face in faces:
            for i in range(4):
                ## Circular index
                j = (i + 1) % 4

                distance = self.calculate_distance(face[i], face[j])
                direction = self.calculate_direction(face[i], face[j], distance)

                vectors.append([distance, direction])
        
        sides = []

        ## Remove duplicate vectors
        for v in vectors:
            direction = v[1]
            
            in_sides = False
            for s in sides:
                if direction == s[1]:
                    in_sides = True
                    break
            
            if not in_sides:
                sides.append(v)


        return sides
                

    def calculate_distance(self, v1, v2):
        # One line 3d pythagoras
        return sum([(v1[i]-v2[i])**2 for i in range(3)])**(1/2)

    def calculate_direction(self, v1, v2, magnitude):
        return [abs(v1[i]-v2[i])/magnitude for i in range(3)]