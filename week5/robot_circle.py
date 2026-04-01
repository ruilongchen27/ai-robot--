import pybullet as p
import pybullet_data
import time
import math

# 连接 PyBullet GUI
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)

# 加载地面和桌子
plane = p.loadURDF("plane.urdf")
table = p.loadURDF("table/table.urdf",[0.5,0,0])

# 加载白色机械臂
robot = p.loadURDF("franka_panda/panda.urdf",[0,0,0],useFixedBase=True)
end_effector = 11  # Panda末端

# 圆参数（在桌面上方2cm）
radius = 0.1
center_x = 0.5
center_y = 0
z = 0.64  # 桌子高度约0.62，加上2cm

prev_pos = None

# 画圆轨迹
for t in range(3000):
    angle = 2*math.pi*t/3000
    x = center_x + radius*math.cos(angle)
    y = center_y + radius*math.sin(angle)
    pos = [x,y,z]

    # 逆运动学求关节角
    jointPoses = p.calculateInverseKinematics(robot,end_effector,pos)

    # 控制机械臂7个关节
    for i in range(7):
        p.setJointMotorControl2(
            robot,
            i,
            p.POSITION_CONTROL,
            jointPoses[i],
            force=500
        )

    # 画红色轨迹
    if prev_pos is not None:
        p.addUserDebugLine(prev_pos,pos,[1,0,0],2)
    prev_pos = pos

    p.stepSimulation()
    time.sleep(1./240.)

# 保持窗口，不自动关闭
while True:
    p.stepSimulation()
    time.sleep(1./240.)