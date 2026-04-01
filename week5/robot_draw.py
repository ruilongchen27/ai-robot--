import pybullet as p
import pybullet_data
import time
import math

# 连接GUI
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)

# 地面和桌子
plane = p.loadURDF("plane.urdf")
table = p.loadURDF("table/table.urdf",[0.5,0,0])

# 白色Panda机械臂
robot = p.loadURDF("franka_panda/panda.urdf",[0,0,0],useFixedBase=True)
end_effector = 11  # 末端

# ----------------------
# 1️⃣ 在桌面上画圆
# ----------------------
radius = 0.1
center = [0.5,0,0.64]  # 桌面上方2cm
steps_circle = 300
prev_pos = None

for t in range(steps_circle+1):
    angle = 2*math.pi*t/steps_circle
    x = center[0] + radius*math.cos(angle)
    y = center[1] + radius*math.sin(angle)
    z = center[2]
    pos = [x,y,z]

    # 逆运动学求关节角
    jointPoses = p.calculateInverseKinematics(robot,end_effector,pos)

    # 控制机械臂
    for i in range(7):
        p.setJointMotorControl2(
            robot,
            i,
            p.POSITION_CONTROL,
            jointPoses[i],
            force=500
        )

    # 画红色轨迹
    if prev_pos:
        p.addUserDebugLine(prev_pos,pos,[1,0,0],2)
    prev_pos = pos

    p.stepSimulation()
    time.sleep(1./240.)

# ----------------------
# 2️⃣ 在桌面上画直线
# ----------------------
start_pos = [0.4,0,0.64]
end_pos   = [0.6,0,0.64]
steps_line = 200
prev_pos = None

for i in range(steps_line+1):
    t = i/steps_line
    # 末端空间线性插值
    x = start_pos[0]*(1-t) + end_pos[0]*t
    y = start_pos[1]*(1-t) + end_pos[1]*t
    z = start_pos[2]
    pos = [x,y,z]

    # 逆运动学求关节角
    jointPoses = p.calculateInverseKinematics(robot,end_effector,pos)

    # 控制机械臂
    for j in range(7):
        p.setJointMotorControl2(
            robot,
            j,
            p.POSITION_CONTROL,
            jointPoses[j],
            force=500
        )

    # 画红色轨迹
    if prev_pos:
        p.addUserDebugLine(prev_pos,pos,[1,0,0],2)
    prev_pos = pos

    p.stepSimulation()
    time.sleep(1./240.)

# 保持窗口
while True:
    p.stepSimulation()
    time.sleep(1./240.)