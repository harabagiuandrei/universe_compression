import numpy as np
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class PhysicsObject:
    def __init__(self, position, properties=None):
        self.position = np.array(position)
        self.properties = properties if properties else {}

    def apply_behavior(self, behavior_name, function, *args):
        if callable(function):
            self.properties[behavior_name] = function(*args)
        else:
            raise ValueError("Behavior function must be callable.")

    def __repr__(self):
        props_str = ".".join([f"{k}({v})" for k, v in self.properties.items()]) if self.properties else ""
        return f"PhysicsObject(pos={self.position}, props={props_str})"

class UniverseZone:
    def __init__(self, size):
        self.size = np.array(size)
        self.behaviors = {}

    def batch_activate(self, activation_function, initial_gravity=0.0):
        activated_particles = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    if activation_function(x, y, z):
                        particle = PhysicsObject((x, y, z), properties={"gravity": initial_gravity})
                        activated_particles.append(particle)
        return activated_particles

    def apply_behavior(self, axis, behavior_name):
        if axis in ['x', 'y', 'z']:
            self.behaviors[axis] = self.behaviors.get(axis, []) + [behavior_name]
        else:
            raise ValueError("Invalid axis. Choose 'x', 'y', or 'z'.")

    def to_compressed_notation(self):
        notation = []
        for axis, length in zip(['x', 'y', 'z'], self.size):
            behaviors = ".".join(self.behaviors.get(axis, []))
            formatted = "." + ".".join([f"{b}()" for b in self.behaviors.get(axis, [])]) if behaviors else ""
            notation.append(f"{{{axis}({length}){formatted}}}")
        return ", ".join(notation)

    @staticmethod
    def from_compressed_notation(notation):
        pattern = re.compile(r"\{([xyz])\((\d+)\)((?:\.[a-zA-Z0-9_]+\(\))*)\}")
        size = {}
        behaviors = {}

        for match in pattern.finditer(notation):
            axis, length, behavior_str = match.groups()
            size[axis] = int(length)
            if behavior_str:
                behaviors[axis] = [b[:-2] for b in behavior_str.split('.') if b]

        uz = UniverseZone((size['x'], size['y'], size['z']))
        uz.behaviors = behaviors
        return uz

    def __repr__(self):
        return f"UniverseZone(size={self.size})"

def spherical_activation(center, radius):
    def activate(x, y, z):
        return np.linalg.norm(np.array([x, y, z]) - np.array(center)) <= radius
    return activate

# PHASE 2 SIM: Visualize anti-gravity spherical zone in 3D
size = (30, 30, 30)
universe = UniverseZone(size)
center = (15, 15, 15)
radius = 8
particles = universe.batch_activate(spherical_activation(center, radius), initial_gravity=9.83)

# Apply anti-gravity effect (subtract gravity)
for p in particles:
    if "gravity" in p.properties:
        p.properties["gravity"] += -9.83

# Visualize affected particles
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

xs, ys, zs = zip(*[p.position for p in particles if p.properties.get("gravity") == 0.0])
ax.scatter(xs, ys, zs, c='red', marker='o', label="zero-gravity zone")

ax.set_xlim(0, size[0])
ax.set_ylim(0, size[1])
ax.set_zlim(0, size[2])
ax.set_title("Anti-Gravity Sphere Simulation")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()
plt.tight_layout()
plt.show()

# Output Notation
notation = "{x(30).gravity()}, {y(30)}, {z(30)}"
universe = UniverseZone.from_compressed_notation(notation)
print("Exported Notation:", universe.to_compressed_notation())
