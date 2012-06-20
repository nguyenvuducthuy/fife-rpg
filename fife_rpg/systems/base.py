# -*- coding: utf-8 -*-
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The base system and functions

.. module:: base
    :synopsis: The base system and functions

.. moduleauthor:: Karsten Bock <KarstenBock@gmx.net>
"""
from bGrease import System

from fife_rpg.exceptions import AlreadyRegisteredError
from fife_rpg.systems import SystemManager

class ClassProperty(property):
    """Class to make class properties"""
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)() # pylint: disable=E1101

class Base(System):
    """Base system for fife-rpg."""

    __registered_as = None
    __dependencies = []

    @ClassProperty
    @classmethod
    def registered_as(cls):
        """Returns the value of registered_as"""
        return cls.__registered_as

    @classmethod
    def register(cls, name, *args, **kwargs):
        """Registers the class as a system

        Args:
            name: The name under which the class should be registered
            *args: Additional arguments to pass to the class constructor
            **kwargs: Additional keyword arguments to pass to the class 
            constructor

        Returns:
            True if the system was registered, False if not.
        """
        try:
            SystemManager.register_system(name, cls(*args, **kwargs))
            cls.__registered_as = name
            for dependency in cls.__dependencies:
                if not dependency.registered_as:
                    dependency.register()
            return True
        except AlreadyRegisteredError as error:
            print error
            return False

