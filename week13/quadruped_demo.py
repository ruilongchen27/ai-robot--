import pybullet as p
import pybullet_data
import time
import numpy as np
import math


class QuadrupedController:
    """简单的四足机器人控制器"""

    def __init__(self, robot_id):
        self.robot_id = robot_id

        # PyBullet Laikago 模型的关节 ID，实际模型不同时需要调整
        self.leg_joints = {
            "LF": [0, 1, 2],
            "RF": [3, 4, 5],
            "LH": [6, 7, 8],
            "RH": [9, 10, 11],
        }

        self.stance_height = 0.3
        self.step_height = 0.05
        self.step_length = 0.1

    def trot_gait(self, t, leg_name, frequency=1.0):
        """生成简化 Trot 步态"""

        if leg_name in ["LF", "RH"]:
            phase = 0
        else:
            phase = np.pi

        cycle_phase = (2 * np.pi * frequency * t + phase) % (2 * np.pi)

        if cycle_phase < np.pi:
            progress = cycle_phase / np.pi
            x = self.step_length * (progress - 0.5)
            z = self.step_height * np.sin(np.pi * progress)
        else:
            progress = (cycle_phase - np.pi) / np.pi
            x = self.step_length * (0.5 - progress)
            z = 0

        hip = 0
        target_height = self.stance_height + z

        thigh = np.arctan2(x, target_height)
        calf = -2 * thigh

        return [hip, thigh, calf]

    def step(self, t, frequency=1.0):
        """执行一帧步态控制"""

        for leg_name, joint_ids in self.leg_joints.items():
            target_angles = self.trot_gait(t, leg_name, frequency)

            for joint_id, angle in zip(joint_ids, target_angles):
                p.setJointMotorControl2(
                    self.robot_id,
                    joint_id,
                    p.POSITION_CONTROL,
                    targetPosition=angle,
                    force=20,
                )


def main():
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)
    p.loadURDF("plane.urdf")

    start_orientation = p.getQuaternionFromEuler([math.pi / 2, 0, math.pi / 2])
    robot_id = p.loadURDF("laikago/laikago_toes.urdf", [0, 0, 0.5], start_orientation)

    controller = QuadrupedController(robot_id)

    t = 0
    dt = 1.0 / 240.0

    print("开始仿真，按 Ctrl+C 停止...")

    try:
        while True:
            controller.step(t, frequency=0.5)
            p.stepSimulation()
            time.sleep(dt)
            t += dt
    except KeyboardInterrupt:
        print("仿真结束")

    p.disconnect()


if __name__ == "__main__":
    main()