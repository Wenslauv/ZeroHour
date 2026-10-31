"""Generates a random blockout arena at /Game/Maps/L_Arena.

Fixed parts: outer walls with an opening to the north, a corridor with DoorSlot
(the door from day 3), PlayerStart in the south-west corner, NavMesh, lighting.
Random parts, driven by a seed: arena size, platforms with ramps, cover walls,
pillars and jump blocks. Obstacles are placed by rejection sampling with spacing
rules, so the floor stays connected for both the player and the AI.

Run in Unreal Editor (Output Log, Cmd):
  py build_arena.py              -> new random layout, the seed is printed to the log
  py build_arena.py --seed 1234  -> reproduce a layout
Or set SEED below and use Tools -> Execute Python Script.

Safe to re-run: everything the script spawns lives in the "Arena" outliner folder
and is rebuilt from scratch on every run. All sizes are in centimeters.
After every run: Build -> Build Paths, so the NavMesh is generated for the new layout.
"""
import math
import random
import sys

import unreal

# ---- Generation criteria -------------------------------------------------
SEED = None                      # None = random; an int reproduces a layout
ARENA_SIZE_RANGE = (3200, 4800)  # width and depth are picked independently
WALL_HEIGHT = 400
MIN_GAP = 250                    # free space between obstacles, well above the AI agent diameter
WALL_CLEARANCE = 200             # free strip along the outer walls
RAMP_ANGLE = 25                  # degrees; the walkable limit is ~44
RAMP_WIDTH = 300
COUNTS = {                       # (min, max) obstacles per type
    "platform": (1, 2),
    "cover": (4, 7),
    "pillar": (2, 4),
    "jump_block": (1, 3),
}
MAX_ATTEMPTS = 200

# ---- Assets ----------------------------------------------------------------
LEVEL_PATH = "/Game/Maps/L_Arena"
FOLDER = "Arena"
CUBE = "/Engine/BasicShapes/Cube"  # 100 cm cube, pivot at the center
MAT_FLOOR = "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray"
MAT_WALL = "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02"
MAT_PROP = "/Game/LevelPrototyping/Materials/MI_PrototypeGrid_TopDark"

NO_ROTATION = unreal.Rotator(roll=0.0, pitch=0.0, yaw=0.0)

level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


# ---- Helpers ---------------------------------------------------------------
def snap(value, step=50):
    return round(value / step) * step


def overlaps(a, b, gap):
    """Axis-aligned rects (x0, y0, x1, y1): True if closer than gap."""
    return not (a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1])


def read_seed():
    if "--seed" in sys.argv:
        return int(sys.argv[sys.argv.index("--seed") + 1])
    if SEED is not None:
        return SEED
    return random.randrange(1, 1_000_000)


class Layout:
    """Tracks occupied floor space and answers 'does this footprint fit?'."""

    def __init__(self, rng, width, depth):
        self.rng = rng
        self.half_w = width / 2
        self.half_d = depth / 2
        self.taken = []     # obstacle footprints, kept MIN_GAP apart
        self.reserved = []  # zones that must stay empty

    def is_free(self, rect):
        lim_x = self.half_w - WALL_CLEARANCE
        lim_y = self.half_d - WALL_CLEARANCE
        if rect[0] < -lim_x or rect[2] > lim_x or rect[1] < -lim_y or rect[3] > lim_y:
            return False
        if any(overlaps(rect, other, MIN_GAP) for other in self.taken):
            return False
        return not any(overlaps(rect, zone, 0) for zone in self.reserved)

    def try_place(self, local_rect):
        """local_rect is relative to the object's center; returns the center or None."""
        for _ in range(MAX_ATTEMPTS):
            cx = snap(self.rng.uniform(-self.half_w, self.half_w))
            cy = snap(self.rng.uniform(-self.half_d, self.half_d))
            rect = (cx + local_rect[0], cy + local_rect[1], cx + local_rect[2], cy + local_rect[3])
            if self.is_free(rect):
                self.taken.append(rect)
                return cx, cy
        return None


def centered(size_x, size_y):
    return (-size_x / 2, -size_y / 2, size_x / 2, size_y / 2)


# ---- Spawning --------------------------------------------------------------
def open_or_create_level():
    if unreal.EditorAssetLibrary.does_asset_exist(LEVEL_PATH):
        level_subsystem.load_level(LEVEL_PATH)
    elif not level_subsystem.new_level(LEVEL_PATH):
        raise RuntimeError(f"Could not create {LEVEL_PATH}")


def clear_previous_build():
    foreign = []
    for actor in actor_subsystem.get_all_level_actors():
        if str(actor.get_folder_path()).startswith(FOLDER):
            actor_subsystem.destroy_actor(actor)
        elif isinstance(actor, unreal.StaticMeshActor):
            foreign.append(actor.get_actor_label())
    if foreign:
        unreal.log_warning(f"{LEVEL_PATH} has {len(foreign)} meshes the generator did not create "
                           f"(e.g. {', '.join(foreign[:5])}); they are left untouched.")


def place(actor, label, sub_folder):
    actor.set_actor_label(label)
    actor.set_folder_path(f"{FOLDER}/{sub_folder}")
    return actor


def spawn(actor_class, location, label, sub_folder, rotation=NO_ROTATION):
    actor = actor_subsystem.spawn_actor_from_class(actor_class, unreal.Vector(*location), rotation)
    return place(actor, label, sub_folder)


def box(label, center, size, material, sub_folder="Blockout", pitch=0.0, yaw=0.0):
    actor = actor_subsystem.spawn_actor_from_object(
        unreal.load_asset(CUBE),
        unreal.Vector(*center),
        unreal.Rotator(roll=0.0, pitch=pitch, yaw=yaw),
    )
    actor.set_actor_scale3d(unreal.Vector(size[0] / 100.0, size[1] / 100.0, size[2] / 100.0))
    actor.static_mesh_component.set_material(0, unreal.load_asset(material))
    return place(actor, label, sub_folder)


# ---- Fixed parts -------------------------------------------------------------
def build_lighting():
    sun = spawn(unreal.DirectionalLight, (0, 0, 1000), "Sun", "Lighting",
                unreal.Rotator(roll=0.0, pitch=-50.0, yaw=35.0))
    sun.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    sun.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property("atmosphere_sun_light", True)

    sky = spawn(unreal.SkyLight, (0, 0, 1200), "SkyLight", "Lighting")
    sky.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    sky.get_component_by_class(unreal.SkyLightComponent).set_editor_property("real_time_capture", True)

    spawn(unreal.SkyAtmosphere, (0, 0, 0), "SkyAtmosphere", "Lighting")
    spawn(unreal.ExponentialHeightFog, (0, 0, 0), "HeightFog", "Lighting")


def build_shell(width, depth):
    """Floor, outer walls with a 3 m opening to the north, and the dead-end corridor."""
    h = WALL_HEIGHT
    hw, hd = width / 2, depth / 2
    box("Floor_Arena", (0, 0, -25), (width, depth, 50), MAT_FLOOR)
    box("Wall_South", (0, -hd - 25, h / 2), (width + 100, 50, h), MAT_WALL)
    box("Wall_East", (hw + 25, 0, h / 2), (50, depth, h), MAT_WALL)
    box("Wall_West", (-hw - 25, 0, h / 2), (50, depth, h), MAT_WALL)
    segment = hw - 100  # from the corner to the opening edge at x = +-150
    box("Wall_North_L", (-(hw + 200) / 2, hd + 25, h / 2), (segment, 50, h), MAT_WALL)
    box("Wall_North_R", ((hw + 200) / 2, hd + 25, h / 2), (segment, 50, h), MAT_WALL)

    # Corridor 3 m wide, 12 m long; the door goes at DoorSlot on day 3
    box("Floor_Corridor", (0, hd + 600, -25), (400, 1200, 50), MAT_FLOOR)
    box("Wall_Corridor_L", (-175, hd + 625, h / 2), (50, 1150, h), MAT_WALL)
    box("Wall_Corridor_R", (175, hd + 625, h / 2), (50, 1150, h), MAT_WALL)
    box("Wall_Corridor_End", (0, hd + 1225, h / 2), (400, 50, h), MAT_WALL)


def build_markers(width, depth, seed):
    hw, hd = width / 2, depth / 2
    spawn(unreal.PlayerStart, (-hw + 400, -hd + 400, 100), "PlayerStart", "Gameplay",
          unreal.Rotator(roll=0.0, pitch=0.0, yaw=45.0))
    spawn(unreal.TargetPoint, (0, hd + 400, 0), "DoorSlot", "Gameplay")
    spawn(unreal.TargetPoint, (0, 0, 0), f"ArenaInfo_seed_{seed}_{int(width)}x{int(depth)}", "Gameplay")


def build_navigation(width, depth):
    hd = depth / 2
    y_min, y_max = -hd - 100, hd + 1300  # arena plus corridor
    size = (width + 200, y_max - y_min, 600)
    nav = spawn(unreal.NavMeshBoundsVolume, (0, (y_min + y_max) / 2, 200), "NavMeshBounds", "Gameplay")
    # The default volume brush is a 200 cm cube
    nav.set_actor_scale3d(unreal.Vector(size[0] / 200.0, size[1] / 200.0, size[2] / 200.0))
    _, extent = nav.get_actor_bounds(False)
    if extent.x < 1000:
        unreal.log_warning("NavMeshBoundsVolume came out without a brush: place one by hand over the arena.")


# ---- Random parts --------------------------------------------------------------
def build_platforms(layout):
    rng = layout.rng
    rad = math.radians(RAMP_ANGLE)
    placed = 0
    for index in range(rng.randint(*COUNTS["platform"])):
        sx, sy = snap(rng.uniform(500, 900)), snap(rng.uniform(400, 700))
        height = snap(rng.uniform(120, 200), 10)
        run = height / math.tan(rad)
        dx, dy = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])  # side the ramp comes down on

        # Footprint = platform + ramp; MIN_GAP around it keeps the ramp foot clear
        x0, y0, x1, y1 = centered(sx, sy)
        x0, x1 = (x0 - run, x1) if dx < 0 else (x0, x1 + run) if dx > 0 else (x0, x1)
        y0, y1 = (y0 - run, y1) if dy < 0 else (y0, y1 + run) if dy > 0 else (y0, y1)
        center = layout.try_place((x0, y0, x1, y1))
        if center is None:
            continue
        cx, cy = center
        box(f"Platform_{index}", (cx, cy, height / 2), (sx, sy, height), MAT_PROP)

        # Ramp slab: top surface goes from the platform edge (z = height) down to the floor
        yaw = math.degrees(math.atan2(-dy, -dx))  # slab X axis points uphill, toward the platform
        top_x = cx + dx * (sx / 2 + run / 2)
        top_y = cy + dy * (sy / 2 + run / 2)
        thickness = 20.0
        normal = (-math.sin(rad) * math.cos(math.radians(yaw)),
                  -math.sin(rad) * math.sin(math.radians(yaw)),
                  math.cos(rad))
        ramp_center = (top_x - normal[0] * thickness / 2,
                       top_y - normal[1] * thickness / 2,
                       height / 2 - normal[2] * thickness / 2)
        box(f"Ramp_{index}", ramp_center, (height / math.sin(rad), RAMP_WIDTH, thickness), MAT_PROP,
            pitch=RAMP_ANGLE, yaw=yaw)
        placed += 1
    return placed


def build_simple(layout, kind, make_size, material):
    """Places boxes of one kind; make_size(rng) -> (size_x, size_y, height)."""
    rng = layout.rng
    placed = 0
    for index in range(rng.randint(*COUNTS[kind])):
        sx, sy, h = make_size(rng)
        center = layout.try_place(centered(sx, sy))
        if center is None:
            continue
        box(f"{kind.title().replace('_', '')}_{index}", (center[0], center[1], h / 2), (sx, sy, h), material)
        placed += 1
    return placed


def cover_size(rng):
    length = snap(rng.uniform(200, 500))
    height = snap(rng.uniform(150, 250), 10)
    return (length, 50, height) if rng.random() < 0.5 else (50, length, height)


def pillar_size(rng):
    side = snap(rng.uniform(100, 200))
    return side, side, 300


def jump_block_size(rng):
    side = snap(rng.uniform(150, 250))
    return side, side, snap(rng.uniform(80, 120), 10)  # low enough to jump on


# ---- Entry point -------------------------------------------------------------
def main():
    seed = read_seed()
    rng = random.Random(seed)
    width = snap(rng.uniform(*ARENA_SIZE_RANGE), 100)
    depth = snap(rng.uniform(*ARENA_SIZE_RANGE), 100)

    layout = Layout(rng, width, depth)
    hw, hd = width / 2, depth / 2
    layout.reserved.append((-hw, -hd, -hw + 800, -hd + 800))  # around PlayerStart
    layout.reserved.append((-400, hd - 600, 400, hd))         # in front of the corridor

    open_or_create_level()
    with unreal.ScopedEditorTransaction("Build ZeroHour arena"):
        clear_previous_build()
        build_lighting()
        build_shell(width, depth)
        stats = {
            "platform": build_platforms(layout),
            "cover": build_simple(layout, "cover", cover_size, MAT_PROP),
            "pillar": build_simple(layout, "pillar", pillar_size, MAT_PROP),
            "jump_block": build_simple(layout, "jump_block", jump_block_size, MAT_PROP),
        }
        build_markers(width, depth, seed)
        build_navigation(width, depth)
    level_subsystem.save_current_level()
    unreal.log(f"Arena built: seed={seed}, size={int(width)}x{int(depth)} cm, placed={stats}. "
               f"Now run Build -> Build Paths, then press P in the viewport to see the NavMesh.")


main()
