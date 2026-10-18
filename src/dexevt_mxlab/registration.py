"""Entry-point callback for registering the external Dex-EVT tasks."""


def register() -> None:
    """Register the walk and whole-body tracking tasks."""
    # Import task modules for their registration side effects; imports are cached.
    import dexevt_mxlab.envs.walk.dexevt  # noqa: F401
    import dexevt_mxlab.envs.wbt.dexevt  # noqa: F401


def register_robots() -> None:
    """Register the package-owned Dex-EVT robot configuration."""
    from motrix_env_core import registry

    from dexevt_mxlab.robots.dexevt import DexEvt

    registry.register_robot_config("dexevt", DexEvt)
