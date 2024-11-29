import math
import matplotlib.pyplot as plt

GRAVITY = 0.0000000000667

class vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def subtract(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return vector(x,y,z)
    
    def add(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return vector(x,y,z)
    
    def multiply(self, scalar):
        x = self.x * scalar
        y = self.y * scalar
        z = self.z * scalar
        return vector(x,y,z)

    def get_size_squared(self):
        return self.x**2 + self.y**2 + self.z**2
    
    def get_scalar(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    

class body:
    def __init__(self, mass, pos_i, v_i):
        self.mass = mass
        #self.previous_velocity = v_i
        #self.previous_position = pos_i
        self.curr_position = pos_i
        self.curr_velocity = v_i
    
    def calculate_force(self, bodies):
        force = vector(0,0,0)
        for body in bodies:
            distance_squared = self.curr_position.subtract(body.curr_position).get_size_squared()
            force_scalar = GRAVITY*body.mass/distance_squared
            distance = math.sqrt(distance_squared)
            distance_vector = body.curr_position.subtract(self.curr_position)
            force_vector = distance_vector.multiply(force_scalar/distance)
            force = force.add(force_vector)
        self.force = force
            
    def update_params(self, bodies, time):
        self.curr_position = self.curr_position.add(self.curr_velocity.multiply(time))
        self.curr_velocity = self.curr_velocity.add(self.force.multiply(time))
        self.calculate_force(bodies)
    
    def get_position(self):
        return self.curr_position

    def get_force(self):
        return self.force

def solar_system():
    earth = body(5.97*(10**24), vector(149000000000,0,0), vector(0, 29700, 0))
    sun = body(1.99*(10**30), vector(0,0,0), vector(0,0,0))
    earth.calculate_force([sun])
    pos_x = []
    pos_y = []
    for t in range(0,31536000,100):
        earth.update_params([sun],100)
        if t % 86400 == 0:
            pos_x.append(earth.get_position().x)
            pos_y.append(earth.get_position().y)
    plt.plot(pos_x,pos_y)
    plt.show()

def two_body():
    earth = body(5.97*(10**24), vector(149000000000,0,0), vector(0, 29700, 0))
    sun = body(1.99*(10**30), vector(0,0,0), vector(0,0,0))
    armageddon = body(1.99*(10**30), vector(1490000000000,0,0), vector(0,0,0))
    
    sun.calculate_force([armageddon])
    armageddon.calculate_force([sun])
    earth.calculate_force([sun, armageddon])
    
    earth_x = []
    earth_y = []

    sun_x = []
    sun_y = []

    armageddon_x = []
    armageddon_y = []

    for t in range(0,3*31536000,100):
        
        earth.update_params([sun, armageddon],100)
        sun.update_params([armageddon], 100)
        armageddon.update_params([sun], 100)

        if t % 86400 == 0:
            earth_x.append(earth.get_position().x)
            earth_y.append(earth.get_position().y)
            sun_x.append(sun.get_position().x)
            sun_y.append(sun.get_position().y)
            armageddon_x.append(armageddon.get_position().x)
            armageddon_y.append(armageddon.get_position().y)

    plt.plot(sun_x,sun_y,color='r',label='sun')
    plt.plot(earth_x,earth_y,color='b',label='earth')
    plt.plot(armageddon_x,armageddon_y,color='g',label='armageddon')
    plt.legend()
    plt.show()

if __name__=='__main__':
    #solar_system() 
    two_body()
