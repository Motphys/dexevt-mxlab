# Copyright Motphys Technology Co., Ltd. 2025, 2026
# SPDX-License-Identifier: Apache-2.0
# Adapted from MotrixLab: package-owned imports and external task registration.

"""External Dex-EVT flat-ground velocity-tracking task."""

from motrix_env_core import registry
from motrix_env_core.base import SimCfg
from motrix_env_core.config.scene import FlatTerrainCfg
from motrix_env_core.manager import ManagerEnv
from motrix_env_core.mdp.rewards import TrackingAngVelZRewardCfg, TrackingLinVelXyRewardCfg
from motrix_env_core.mdp.terminations import CollidingTerminationCfg

from dexevt_mxlab.envs.common.scene import StandardSceneObjsCfg
from dexevt_mxlab.envs.walk.cfg import (
    HumanoidVelocityTrackingManagerEnvCfg,
    HumanoidWalkSceneCfg,
    WalkRewardsCfg,
    WalkTerminationsCfg,
)
from dexevt_mxlab.envs.walk.mdp.rewards import (
    FeetPhaseRewardCfg,
    PenaltyActionRateRewardCfg,
    PenaltyCloseFeetXyRewardCfg,
    PoseRewardCfg,
)
from dexevt_mxlab.robots.dexevt import DexEvt

# Dex-EVT-specific collision inventory, owned by this external task.
_DEX_EVT_TERMINATION_GEOMS = (
    "pelvis_collision",
    "hip_pitch_l_link_collision",
    "hip_yaw_l_link_collision",
    "knee_pitch_l_link_collision",
    "hip_pitch_r_link_collision",
    "hip_yaw_r_link_collision",
    "knee_pitch_r_link_collision",
    "waist_pitch_link_collision",
    "shoulder_yaw_l_link_collision",
    "wrist_pitch_l_link_collision",
    "left_tcp_link_collision",
    "shoulder_yaw_r_link_collision",
    "wrist_pitch_r_link_collision",
    "right_tcp_link_collision",
)


def _make_dex_evt_rewards() -> WalkRewardsCfg:
    return WalkRewardsCfg(
        tracking_lin_vel=TrackingLinVelXyRewardCfg(command_name="walk", sigma=0.25, weight=2.0),
        tracking_ang_vel=TrackingAngVelZRewardCfg(command_name="walk", sigma=0.25, weight=1.5),
        penalty_action_rate=PenaltyActionRateRewardCfg(weight=-2.0),
        feet_phase=FeetPhaseRewardCfg(
            sole_l_site="left_foot_contact_point",
            sole_r_site="right_foot_contact_point",
            weight=5.0,
        ),
        penalty_close_feet_xy=PenaltyCloseFeetXyRewardCfg(close_feet_threshold=0.15, weight=-10.0),
        pose=PoseRewardCfg(
            pose_weights={
                "hip_pitch_l_joint": 0.01,
                "hip_roll_l_joint": 1.0,
                "hip_yaw_l_joint": 5.0,
                "knee_pitch_l_joint": 0.01,
                "ankle_pitch_l_joint": 5.0,
                "ankle_roll_l_joint": 5.0,
                "hip_pitch_r_joint": 0.01,
                "hip_roll_r_joint": 1.0,
                "hip_yaw_r_joint": 5.0,
                "knee_pitch_r_joint": 0.01,
                "ankle_pitch_r_joint": 5.0,
                "ankle_roll_r_joint": 5.0,
                "waist_yaw_joint": 50.0,
                "waist_roll_joint": 50.0,
                "waist_pitch_joint": 50.0,
                "shoulder_pitch_l_joint": 50.0,
                "shoulder_roll_l_joint": 50.0,
                "shoulder_yaw_l_joint": 50.0,
                "elbow_pitch_l_joint": 50.0,
                "shoulder_pitch_r_joint": 50.0,
                "shoulder_roll_r_joint": 50.0,
                "shoulder_yaw_r_joint": 50.0,
                "elbow_pitch_r_joint": 50.0,
            },
            weight=-0.5,
        ),
    )


@registry.envcfg("dexevt-walk-flat")
def make_dex_evt_walk_flat_cfg() -> HumanoidVelocityTrackingManagerEnvCfg:
    """Control the Dex-EVT humanoid to walk on flat ground."""
    return HumanoidVelocityTrackingManagerEnvCfg(
        scene=HumanoidWalkSceneCfg(
            objs=StandardSceneObjsCfg(
                floor=FlatTerrainCfg(
                    material="mat_ground",
                    friction=(0.8, 0.005, 0.0001),
                ),
                robot=DexEvt(translation=(0.0, 0.0, 0.9785)),
            ),
        ),
        rewards=_make_dex_evt_rewards(),
        terminations=WalkTerminationsCfg(
            colliding=CollidingTerminationCfg(
                termination_geoms=_DEX_EVT_TERMINATION_GEOMS,
                ground_geom="floor",
            )
        ),
        sim=SimCfg(dt=0.005, solver_iterations=6, solver_tolerance=0.0001),
    )


registry.env("dexevt-walk-flat")(ManagerEnv)
