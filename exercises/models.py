"""
models.py
"""

import json
from django.db import models
import subprocess

StatusChoice = (
    ('ACTIVE', "ACTIVE"),
    ('INACTIVE', "INACTIVE"),
    ('PROTOTYPE', "PROTOTYPE")
)

VisualizationType = (
    ('none', "None"),
    ('console', "Console"),
    ('gazebo_gra', "Gazebo GRA"),
    ('gazebo_rae', "Gazebo RAE"),
    ('gzsim_gra', "Gz Sim GRA"),
    ('gzsim_rae', "Gz Sim RAE"),
    ('physic_gra', "Physic GRA"),
    ('physic_rae', "Physic RAE")
)

UniverseType = (
    ('none', "None"),
    ('gazebo', "Gazebo"),
    ('drones', "Gazebo Drones"),
    ('physical', "Physical")
)

RosVersion = (
    ('ROS1', "ROS1"),
    ('ROS2', "ROS2")
)


class Universe(models.Model):
    """
    Modelo Universe para RoboticsCademy
    """
    name = models.CharField(max_length=100, blank=False, unique=True)
    launch_file_path = models.CharField(max_length=200, blank=False)
    ros_version = models.CharField(
        max_length=4, choices=RosVersion, default="none")
    visualization = models.CharField(
        max_length=50,
        choices=VisualizationType,
        default="none",
        blank=False
    )
    world = models.CharField(
        max_length=50,
        choices=UniverseType,
        default="none",
        blank=False
    )

    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = '"universes"'

# Create your models here.


class Exercise(models.Model):
    """
    RoboticsCademy Exercise model
    """
    exercise_id = models.CharField(max_length=40, blank=False, unique=True)
    name = models.CharField(max_length=40, blank=False, unique=True)
    description = models.CharField(max_length=400, blank=False)
    tags = models.CharField(
        max_length=2000,
        default=json.dumps({'tags': ""})
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoice,
        default="ACTIVE"
    )
    worlds = models.ManyToManyField(Universe, default=None, db_table='"exercises_universes"')
    template = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return str(self.name)

    @property
    def context(self):
        """
        Build and return context
        """
        configurations = []

        output = subprocess.check_output(['bash', '-c', 'echo $ROS_VERSION'])
        output_str = output.decode('utf-8')
        if output_str.strip() == '1':
            ros_version = 'ROS1'
        else:
            ros_version = 'ROS2'

        for world in self.worlds.all():
            if world.ros_version == ros_version:
                config = {
                    "name": world.name,
                    "launch_file_path": world.launch_file_path,
                    "ros_version": world.ros_version,
                    "visualization": world.visualization,
                    "world": world.world,
                    "template": self.template,
                    "exercise_id":self.exercise_id
                }
                configurations.append(config)
        
        # If empty worlds add one by default
        if len(configurations) == 0:
            config = {
                "name": None,
                "launch_file_path": None,
                "ros_version": None,
                "visualization": "console",
                "world": None,
                "template": self.template,
                "exercise_id":self.exercise_id
            }
            configurations.append(config)

        context = {
            'exercise_base': "exercise_base_2_RA.html",
            'exercise_id': self.exercise_id,
            'exercise_config': configurations,
        }
        print(context)
        return context
    
    class Meta:
        db_table = '"exercises"'
