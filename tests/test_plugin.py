"""Lightweight contracts for the installed external robot/environment plugin."""

from pathlib import Path
from xml.etree import ElementTree

import numpy as np
import pytest
from motrix_env_core import registry
from motrix_env_core.manager import ManagerBasedEnvCfg

from dexevt_mxlab.envs.wbt.motion.library import MotionLibrary
from dexevt_mxlab.robots.dexevt import DexEvt

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("env_id", ["dexevt-walk-flat", "dexevt-wbt-dance"])
def test_installed_environment_discovery_and_independent_configs(env_id):
    first = registry.make_env_config(env_id)
    second = registry.make_env_config(env_id)
    assert isinstance(first, ManagerBasedEnvCfg)
    assert isinstance(first.scene.objs.robot, DexEvt)
    first.validate()
    first.scene.objs.robot.actuators.clear()
    assert second.scene.objs.robot.actuators


def test_robot_discovery_and_model_resources():
    robot = registry.make_robot_config("dexevt")
    assert isinstance(robot, DexEvt)
    model = Path(robot.model.file)
    root = ElementTree.parse(model).getroot()
    for mesh in root.findall(".//mesh"):
        assert (model.parent / mesh.attrib["filename"]).is_file()
    joint_names = {joint.attrib["name"] for joint in root.findall("joint")}
    assert set(robot.actuators) <= joint_names


def test_bundled_motion_matches_robot_mapping():
    cfg = registry.make_env_config("dexevt-wbt-dance")
    motion = cfg.commands.motion
    clip = MotionLibrary(
        motion.motion_files,
        joint_names=list(motion.joint_names),
        tracked_body_names=motion.tracked_body_names,
        reference_body_name=motion.reference_body_name,
        root_body_name=cfg.scene.objs.robot.resolved_base_link_name,
        fps=round(1 / cfg.ctrl_dt),
        extension_channels=motion.extension_channels,
    ).assemble()
    assert clip.joint_pos.shape[0] > 0
    assert clip.joint_pos.shape[1] == len(motion.joint_names)
    assert clip.tracked_bodies_pos_w.shape[1] == len(motion.tracked_body_names)
    assert np.isfinite(clip.joint_pos).all()
    assert set(motion.joint_names) <= set(cfg.scene.objs.robot.actuators)
