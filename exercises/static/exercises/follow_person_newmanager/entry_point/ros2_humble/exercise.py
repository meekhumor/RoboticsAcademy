import os.path
from typing import Callable

from src.manager.libs.applications.compatibility.exercise_wrapper_ros2_teleop import CompatibilityExerciseWrapperTeleopRos2


class Exercise(CompatibilityExerciseWrapperTeleopRos2):

    def __init__(self, circuit: str, update_callback: Callable):
        current_path = os.path.dirname(__file__)

        super(Exercise, self).__init__(exercise_command=f"{current_path}/../../python_template/ros2_humble/exercise.py 0.0.0.0",
                                       gui_command=f"{current_path}/../../python_template/ros2_humble/gui.py 0.0.0.0 {circuit}",
                                       teleop_command=f"{current_path}/../../python_template/ros2_humble/person_teleoperator.py 0.0.0.0",
                                       update_callback=update_callback)
