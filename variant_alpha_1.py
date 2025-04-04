import numpy as np
import re

class PhysicsObject:
    def __init__(self, position, properties=None):
        self.position = np.array(position)  # (x, y, z) coordinates
        self.properties = properties if properties else {}

    def apply_behavior(self, behavior_name, function, *args):
        """Apply a callable function to modify the object's behavior."""
        if callable(function):
            #TODO:aici se seteaza un STATE al function peste *args??
            self.properties[behavior_name] = function(*args)
        else:
            raise ValueError("Behavior function must be callable.")

    #TODO:
    # def apply_behaviour_multiple(self,behavior_list,function,*args)

    def __repr__(self):
        return f"PhysicsObject(pos={self.position}, props={self.properties})"

class UniverseZone:
    def __init__(self, size):
        """Represents a compressed universe zone with lazy particle instantiation."""
        self.size = np.array(size)  # (x_count, y_count, z_count)
    
    def batch_activate(self, activation_function):
        """Activates only the particles that match the activation function criteria."""
        activated_particles = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    if activation_function(x, y, z):  # Apply function to determine activation
                        activated_particles.append(PhysicsObject((x, y, z)))
        return activated_particles
    
    def iterate_particles(self):
        """Iterates over particles in the zone, instantiating PhysicsObjects lazily."""
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    yield PhysicsObject((x, y, z))

    def to_compressed_notation(self):
        """Exports the universe zone to {x(N).behavior1().behavior2(), y(N), z(N)} format."""
        notation = []
        for axis, length in zip(['x', 'y', 'z'], self.size):
            # behaviors = ".".join(self.behaviors.get(axis, []))
            # # behaviors = behaviors + "()"
            # notation.append(f"{{{axis}({length}){'.' + behaviors if behaviors else ''}}}")
            behaviors = "".join([f".{b}()" for b in self.behaviors.get(axis, [])])
            notation.append(f"{{{axis}({length}){behaviors}}}")
        return ", ".join(notation)

    @staticmethod
    def from_compressed_notation(notation):
        """Creates a UniverseZone object from {x(N), y(N), z(N)} format."""
        # pattern = re.compile(r"\{([xyz])\((\d+)\)(?:\.(\w+))?\}")

        #TODO:regandeste patterns aici ca sa nu se mai faca un regex secundar in "if behavior:"
        pattern = re.compile(r"\{([xyz])\((\d+)\)((?:\.[a-zA-Z0-9_]+\(\))*)\}")

        size = {}
        behaviors = {}
        
        for match in pattern.finditer(notation):
            print("one match inside universe compression createFrom")
            print(match)
            axis, length, behavior = match.groups()
            size[axis] = int(length)
            if behavior:
                behaviors[axis] = re.findall(r"\.[a-zA-Z0-9_]+\(\)", behavior)  # Extract individual behaviors
                behaviors[axis] = [b[1:-2] for b in behaviors[axis]]  # Remove leading '.' and trailing '()'
                # behaviors[axis] = behavior.split('.')
        
        uz = UniverseZone((size['x'], size['y'], size['z']))
        uz.behaviors = behaviors
        return uz
    
    def __repr__(self):
        return f"UniverseZone(size={self.size})"

# Example functions for different behaviors
def fsinusoidal(x):
    return np.sin(x)

def feinstein_gravity(mass1, mass2, distance):
    G = 6.67430e-11  # Gravitational constant
    return G * (mass1 * mass2) / (distance ** 2) if distance != 0 else 0

# Example activation function (wave pattern or explosion)
def spherical_wave_activation(x, y, z, center=(5, 5, 5), radius=3):
    return np.linalg.norm(np.array([x, y, z]) - np.array(center)) <= radius

# Creating a universe zone of 10x10x10 (compressed representation)
universe = UniverseZone((10, 10, 10))

particleIterator = 10
particleCounter = 0

# Iterating over a few particles in the universe
for particle in universe.iterate_particles():
    particle.apply_behavior("wave", fsinusoidal, np.pi/4)
    particle.apply_behavior("gravity", feinstein_gravity, 10, 20, 5)
    print("Universe 1 - ")
    print(particle)
    # if particleCounter+=1 > particleCounter:
        # break  # Only printing one for demonstration
    break

universe2 = UniverseZone((10, 10, 10))

# Activating particles based on spherical wave propagation
active_particles = universe2.batch_activate(lambda x, y, z: spherical_wave_activation(x, y, z))

# Applying behaviors to activated particles
for particle in active_particles:
    particle.apply_behavior("wave", np.sin, np.pi/4)
    print("Universe 2 - ")
    print(particle)

notation = "{x(1000000).wave().gravity()},{y(1000000)},{z(1000000)}"
#TODO:in aceasta instantiere, trebuie sa fim siguri ca un iterate_particles() stie de wave si gravity pentru X

universe3 = UniverseZone.from_compressed_notation(notation)
print("Parsed UniverseZone3:", universe3)
print("Exported Notation3:", universe3.to_compressed_notation())
