import maya.cmds as cmds

# --------------------- NEW SCENE ---------------------
cmds.file(new=True, force=True)

# --------------------- ZIGZAG TRACK ---------------------
# Define zigzag points (shorter track)
track_points = [
    (-20, 0, -40), (-10, 0, -30), (10, 0, -20), (-10, 0, -10),
    (10, 0, 0), (-10, 0, 10), (10, 0, 20), (-10, 0, 30), (20, 0, 40)
]

track = cmds.curve(p=track_points, d=1, name='ZigZagTrack')

# Track material
track_mat = cmds.shadingNode('lambert', asShader=True, name='TrackMat')
cmds.setAttr(track_mat+".color", 0.2,0.2,0.2, type="double3")  # Dark gray
cmds.select(track)
cmds.hyperShade(assign=track_mat)

# --------------------- CAR BODY ---------------------
car = cmds.polyCube(w=2, h=1, d=4, name='Car_Body')[0]
cmds.move(0, 1, -40, car)

body_mat = cmds.shadingNode('blinn', asShader=True, name='CarBodyMat')
cmds.setAttr(body_mat+".color", 1,0,0, type="double3")  # Red
cmds.setAttr(body_mat+".specularColor",1,1,1, type="double3")
cmds.setAttr(body_mat+".eccentricity",0.2)
cmds.select(car)
cmds.hyperShade(assign=body_mat)

# --------------------- WINDOWS ---------------------
window = cmds.polyCube(w=1.8, h=0.5, d=3.5, name='Car_Window')[0]
cmds.move(0,1.5,-40, window)
window_mat = cmds.shadingNode('blinn', asShader=True, name='WindowMat')
cmds.setAttr(window_mat+".color", 0,0,0.2, type="double3")
cmds.setAttr(window_mat+".transparency",0.5,0.5,0.5, type="double3")
cmds.select(window)
cmds.hyperShade(assign=window_mat)
cmds.parent(window, car)

# --------------------- WHEELS ---------------------
wheel_positions = [(0.8,0.25,1.5), (-0.8,0.25,1.5), (0.8,0.25,-1.5), (-0.8,0.25,-1.5)]
wheels = []

wheel_mat = cmds.shadingNode('blinn', asShader=True, name='WheelMat')
cmds.setAttr(wheel_mat+".color",0.05,0.05,0.05, type="double3")
cmds.setAttr(wheel_mat+".specularColor",0.5,0.5,0.5,type="double3")

for i,pos in enumerate(wheel_positions):
    wheel = cmds.polyCylinder(r=0.5,h=0.5,sx=20,sy=1,sz=1,name='Wheel_'+str(i))[0]
    cmds.move(pos[0], pos[1], pos[2], wheel)
    cmds.rotate(90,0,0, wheel)
    cmds.parent(wheel, car)
    cmds.select(wheel)
    cmds.hyperShade(assign=wheel_mat)
    wheels.append(wheel)

# --------------------- CAMERA ---------------------
camera = cmds.camera(name='GameCamera')[0]
cmds.move(0,8,-20, camera)
cmds.aimConstraint(car, camera)

# --------------------- PATH ANIMATION ---------------------
motion_path = cmds.pathAnimation(car, c=track, fractionMode=True, follow=True,
                                 followAxis='x', upAxis='y',
                                 worldUpType='vector', worldUpVector=(0,1,0))
cmds.playbackOptions(minTime=1, maxTime=200)
cmds.setAttr(motion_path+'.uValue', 0)

# --------------------- MOVEMENT FUNCTIONS ---------------------
speed = 0.01  # slightly faster for shorter track

def move_forward(*args):
    u = cmds.getAttr(motion_path+'.uValue')
    u += speed
    if u > 1: u = 0
    cmds.setAttr(motion_path+'.uValue', u)
    for w in wheels:
        cmds.rotate(speed*360,0,0,w, relative=True)

def move_backward(*args):
    u = cmds.getAttr(motion_path+'.uValue')
    u -= speed
    if u < 0: u = 1
    cmds.setAttr(motion_path+'.uValue', u)
    for w in wheels:
        cmds.rotate(-speed*360,0,0,w, relative=True)

def turn_left(*args):
    cmds.rotate(0,5,0,car, relative=True)

def turn_right(*args):
    cmds.rotate(0,-5,0,car, relative=True)

# --------------------- UI CONTROLS ---------------------
if cmds.window('carUI', exists=True):
    cmds.deleteUI('carUI')

window = cmds.window('carUI', title='ZigZag Racing Car', widthHeight=(300,220))
cmds.columnLayout(adjustableColumn=True)
cmds.button(label='Forward', command=move_forward, bgc=(0.6,0.9,0.6))
cmds.button(label='Backward', command=move_backward, bgc=(0.9,0.6,0.6))
cmds.button(label='Turn Left', command=turn_left, bgc=(0.6,0.6,0.9))
cmds.button(label='Turn Right', command=turn_right, bgc=(0.9,0.9,0.6))
cmds.showWindow(window)

print("Zigzag short racing track ready! Drive the car using buttons.")
