# -*- coding: utf-8 -*-
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This package is based on the gamescene classes of PARPG

"""This module contains the generic controller and view to display a
:class:`fife_rpg.map.GameMap`.

.. module:: game_scene
    :synopsis: The generic controller and view to display a fife_rpg map.

.. moduleauthor:: Karsten Bock <KarstenBock@gmx.net>
"""
from abc import ABCMeta, abstractmethod

from fife import fife
from fife.fife import InstanceRenderer

from fife_rpg import ViewBase
from fife_rpg import ControllerBase


class BaseOutliner(object):
    """Determines the outline of an instance"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data(self, world, identifier):
        """Determines whether an instance should be outline and the data
        used for the outline.

        Args:
            world: The world

            identifier: The name of the instance

        Returns: The data as a list, if the instance should be
        outlined. None, if it should not.
        """


class SimpleOutliner(BaseOutliner):
    """Outliner that determines the outline based on a list of identifiers
    to ignore and a single data element for instances that should be outlined.

    Properties:
        outline_data: A tuple of values for the outlines. It is in the order:
        (Red, Green, Blue, Width, Threshold)

        outline_ignore: A list of identifiers to ignore when drawing outlines
    """

    def __init__(self, outline_data=None, outline_ignore=None):
        self.outline_data = outline_data or (255, 255, 255, 1)
        self.__outline_ignore = outline_ignore or []

    @property
    def outline_ignore(self):
        """Returns outline_ignore"""
        return self.__outline_ignore

    def get_data(self, world, identifier):
        """Determines whether an instance should be outline and the data
        used for the outline.

        Args:
            world: The world

            identifier: The name of the instance

        Returns: The data as a list, if the instance should be
        outlined. None, if it should not.
        """
        if identifier in self.outline_ignore:
            return None
        return self.outline_data


class GameSceneListener(fife.IMouseListener):
    """The game listener.

    Handle mouse events in relation
    with game process.

    Properties:
        engine: The FIFE engine

        gamecontroller: A :class:`fife_rpg.game_scene.GameSceneController`

        eventmanager: The engines eventmanager. A :class:`fife.EventManager`

        is_outlined: If true then outlines for instances will be drawn.
    """

    def __init__(self, engine, gamecontroller=None):
        self.engine = engine
        self.gamecontroller = gamecontroller

        self.eventmanager = self.engine.getEventManager()
        fife.IMouseListener.__init__(self)
        self.is_outlined = False

    @property
    def outline_ignore(self):
        """Returns outline_ignore"""
        return self.__outline_ignore

    def activate(self):
        """Makes the listener receive events"""
        self.eventmanager.addMouseListener(self)

    def deactivate(self):
        """Makes the listener receive events"""
        self.eventmanager.removeMouseListener(self)

    def mousePressed(self, event):  # pylint: disable-msg=C0103,W0221
        """Called when a mouse button was pressed.

        Args:
            event: The mouse event
        """
        pass

    def mouseMoved(self, event):  # pylint: disable-msg=C0103,W0221
        """Called when the mouse was moved.

        Args:
            event: The mouse event
        """
        if self.is_outlined:
            controller = self.gamecontroller
            if controller is None:
                return
            game_map = controller.application.current_map
            if game_map:
                renderer = InstanceRenderer.getInstance(game_map.camera)

                renderer.removeAllOutlines()

                point = fife.ScreenPoint(event.getX(), event.getY())
                actor_instances = game_map.get_instances_at(
                                                point,
                                                game_map.get_layer("actors"))

                for instance in actor_instances:
                    data = controller.outliner.get_data(
                                                controller.application.world,
                                                instance.getId()
                                            )
                    if data is not None:
                        renderer.addOutlined(instance, *data)

    def mouseReleased(self, event):  # pylint: disable-msg=C0103,W0221
        """Called when a mouse button was released.

        Args:
            event: The mouse event
        """
        pass

    def mouseDragged(self, event):  # pylint: disable-msg=C0103,W0221
        """Called when the mouse is moved while a button is being pressed.

        Args:
            event: The mouse event
        """
        pass

    def mouseWheelMovedUp(self, event):  # pylint: disable-msg=W0221, C0103
        """Called when the mouse wheel is moved upwards

        Args:
            event: The mouse event
        """
        pass

    def mouseWheelMovedDown(self, event):  # pylint: disable-msg=W0221, C0103
        """Called when the mouse wheel is moved downwards

        Args:
            event: The mouse event
        """
        pass


class GameSceneView(ViewBase):
    """The view responsible for showing the in-game gui

    Properties:
        application: A :class:`fife_rpg.rpg_application.RPGApplication`
        instance
    """

    def __init__(self, application):
        ViewBase.__init__(self, application)


class GameSceneController(ControllerBase):
    """Handles the input for a game scene

    Properties:
        view: A :class:`fife_rpg.game_scene.GameSceneView`

        application: A :class:`fife_rpg.rpg_application.RPGApplication`

        listener: The listener used by the game scene

        outliner: The outliner that will be used to determine outlines
    """

    def __init__(self, view, application, outliner=None, listener=None):
        ControllerBase.__init__(self, view, application)
        self.outliner = outliner or SimpleOutliner()
        self.listener = listener or GameSceneListener(application.engine,
                                                      self)

    def on_activate(self):
        """Being called when the Mode is activated"""
        self.listener.gamecontroller = self
        self.listener.activate()

    def on_deactivate(self):
        """Being called when the Mode is deactivated"""
        self.listener.deactivate()

    def pump(self, time_delta):
        """Performs actions every frame

        Args:
            time_delta: Time that passed since the last call
        """
        ControllerBase.pump(self, time_delta)
