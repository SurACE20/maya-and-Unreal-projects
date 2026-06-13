import maya.cmds as cmds

# ==================================================
# RESET SCENE
# ==================================================
cmds.file(new=True, force=True)
cmds.currentUnit(time='ntsc')
cmds.playbackOptions(min=1, max=900)

# ==================================================
# CREATE SMOOTH ZIGZAG PATH
# ==================================================
path_points = [
    (-40, 0, 0),
    (-28, 0, 15),
    (-10, 0, -15),
    (5, 0, 18),
    (20, 0, -18),
    (35, 0, 0)
]

race_path = cmds.curve(
    p=path_points,
    d=3,
    name="racePath"
)

# ==================================================
# CREATE WIDE RACETRACK
# ==================================================
track = cmds.polyPlane(
    w=120,
    h=50,
    sx=1,
    sy=1,
    name="raceTrack"
)[0]

cmds.rotate(-90, 0, 0, track)
cmds.move(0, -0.05, 0, track)
cmds.setAttr(track + ".overrideEnabled", 1)
cmds.setAttr(track + ".overrideRGBColors", 1)
cmds.setAttr(track + ".overrideColorRGB", 0.4, 0.7, 1.0)  # Light blue track

# ==================================================
# TRACK SIDE BARRIERS
# ==================================================
barrier_group = cmds.group(empty=True, name="barriers_grp")

for x in range(-40, 41, 5):
    for z in (-25, 25):
        barrier = cmds.polyCube(w=3, h=1.2, d=0.8, name=f"barrier_{x}_{z}")[0]
        cmds.move(x, 0.6, z, barrier)
        cmds.parent(barrier, barrier_group)
        cmds.setAttr(barrier + ".overrideEnabled", 1)
        cmds.setAttr(barrier + ".overrideRGBColors", 1)
        cmds.setAttr(barrier + ".overrideColorRGB", 1, 0.2, 0.2)

# ==================================================
# MODERN CAR BODY WITH RED & GREEN
# ==================================================
car_body = cmds.polyCube(w=3.5, h=1, d=7, name="car_body")[0]
cmds.move(-40, 0.8, 0, car_body)
cmds.setAttr(car_body + ".overrideEnabled", 1)
cmds.setAttr(car_body + ".overrideRGBColors", 1)
cmds.setAttr(car_body + ".overrideColorRGB", 1.0, 0.1, 0.1)  # Base red

# Add green stripe using another cube slightly smaller on top
green_stripe = cmds.polyCube(w=0.5, h=0.02, d=7, name="green_stripe")[0]
cmds.move(-40, 1.0, 0, green_stripe)
cmds.parent(green_stripe, car_body)
cmds.setAttr(green_stripe + ".overrideEnabled", 1)
cmds.setAttr(green_stripe + ".overrideRGBColors", 1)
cmds.setAttr(green_stripe + ".overrideColorRGB", 0.0, 1.0, 0.0)  # Bright green stripe

# ==================================================
# CAR ROOF (DARK)
# ==================================================
car_roof = cmds.polyCube(w=2.2, h=0.6, d=3.5, name="car_roof")[0]
cmds.move(-40, 1.2, 0, car_roof)
cmds.parent(car_roof, car_body)
cmds.setAttr(car_roof + ".overrideEnabled", 1)
cmds.setAttr(car_roof + ".overrideRGBColors", 1)
cmds.setAttr(car_roof + ".overrideColorRGB", 0.05, 0.05, 0.05)

# ==================================================
# LARGER WHEELS
# ==================================================
wheel_positions = [
    (1.6, 0.5, 2.8),
    (-1.6, 0.5, 2.8),
    (1.6, 0.5, -2.8),
    (-1.6, 0.5, -2.8)
]

wheels = []
for i, pos in enumerate(wheel_positions):
    wheel = cmds.polyCylinder(r=0.7, h=0.5, sx=24, name=f"wheel_{i+1}")[0]
    cmds.rotate(90, 0, 0, wheel)
    cmds.move(-40 + pos[0], pos[1], pos[2], wheel)
    cmds.parent(wheel, car_body)
    wheel_full_path = cmds.ls(wheel, long=True)[0]
    cmds.setAttr(wheel_full_path + ".overrideEnabled", 1)
    cmds.setAttr(wheel_full_path + ".overrideRGBColors", 1)
    cmds.setAttr(wheel_full_path + ".overrideColorRGB", 0, 0, 0)  # Black wheels
    wheels.append(wheel)

# ==================================================
# GROUP CAR
# ==================================================
car_group = cmds.group(car_body, name="car_grp")

# ==================================================
# MOTION PATH
# ==================================================
cmds.pathAnimation(
    car_group,
    c=race_path,
    follow=True,
    followAxis="x",
    upAxis="y",
    worldUpType="vector",
    worldUpVector=(0, 1, 0),
    startTimeU=1,
    endTimeU=900
)

# ==================================================
# CAMERA
# ==================================================
camera = cmds.camera(name="raceCamera")[0]
cmds.move(0, 50, -95, camera)
cmds.rotate(-30, 0, 0, camera)

# ==================================================
# LIGHTING
# ==================================================
sun = cmds.directionalLight(name="sunLight")[0]
cmds.rotate(-45, 30, 0, sun)

# ==================================================
# DONE
# ==================================================
print("====================================")
print("SUCCESS:")
print("- Car is red with green stripe")
print("- Track is light blue with smooth zigzag")
print("- Modern car wheels and body")
print("- No Script Editor errors")
print("Switch to 'raceCamera' and press PLAY")
print("====================================")
