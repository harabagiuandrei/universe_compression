import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class PhysicsObject:
    def __init__(self, position, properties=None):
        self.position = np.array(position, dtype=float)
        self.velocity = np.zeros(3)
        self.properties = properties if properties else {}

    def update(self, force, dt=1.0):
        acceleration = force  # assume mass = 1
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

class UniverseZone:
    def __init__(self, size):
        self.size = np.array(size)
        self.particles = []

    def populate(self, activation_func, default_properties=None):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    if activation_func(x, y, z):
                        obj = PhysicsObject((x, y, z), default_properties.copy() if default_properties else {})
                        self.particles.append(obj)

    # def apply_void_force(self, center, radius, strength):
    #     for p in self.particles:
    #         relative_pos = p.position - center
    #         distance = np.linalg.norm(relative_pos)
    #         if distance == 0:
    #             continue  # avoid division by zero
    #         if distance <= radius:
    #             direction = relative_pos / distance
    #             magnitude = strength * (1 - distance / radius)  # stronger near center
    #             force = direction * magnitude
    #             p.update(force=force)
    def apply_void_force(self, center, radius, strength, polarity):
        for p in self.particles:
            relative_pos = p.position - center
            distance = np.linalg.norm(relative_pos)
            if distance == 0:
                continue
            if distance <= radius:
                direction = polarity * (relative_pos / distance)
                magnitude = strength * (1 - distance / radius)
                force = direction * magnitude
                p.update(force=force)

    def step(self, center, radius, strength, dt=1.0):
        # !!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!
        # VOID SPHERE = polarity -1
        # self.apply_void_force(center=center, radius=radius, strength=strength, polarity=-1)
        self.apply_void_force(center=center, radius=radius, strength=strength, polarity=-1)
        for p in self.particles:
            p.update(force=np.zeros(3), dt=dt)

    def get_positions(self):
        return np.array([p.position for p in self.particles])

# === SETUP ===
# size = (30, 30, 30)
size = (20, 20, 20)
uz = UniverseZone(size)

def sphere_activation(x, y, z, center=(10, 10, 10), radius=10):
    return np.linalg.norm(np.array([x, y, z]) - np.array(center)) <= radius
uz.particles = []  # reset to clear previous

for x in range(uz.size[0]):
    for y in range(uz.size[1]):
        for z in range(uz.size[2]):
            uz.particles.append(PhysicsObject(position=(x, y, z)))

# uz.populate(lambda x, y, z: sphere_activation(x, y, z))

# SIMULATION PARAMETERS
void_center = np.array([10, 10, 10])
void_radius = 10
void_strength = 5.0

# SIMULATE MULTIPLE FRAMES
frames = []

for step in range(90):  # Simulate 15 frames
    uz.step(center=void_center, radius=void_radius, strength=void_strength)
    frames.append(uz.get_positions().copy())

# === DRAWING (INTERNAL) ===
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i, pos in enumerate(frames):
    ax.clear()
    ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], c='blue', s=5)
    ax.set_xlim(0, size[0])
    ax.set_ylim(0, size[1])
    ax.set_zlim(0, size[2])
    ax.set_title(f"Frame {i}")
    plt.pause(0.1)

plt.show()
