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

#  This module is based on the scriptingsystem module from PARPG

"""The look action prints the description of the target

.. module:: look
    :synopsis: Prints the description of the target
.. moduleauthor:: Karsten Bock <KarstenBock@gmx.net>
"""

from fife_rpg.actions.base import Base
from fife_rpg.components.description import Description

class LookAction(Base):
    """Action for unlocking lockables"""

    dependencies = [Description]

    def __init__(self, controller, agent, target, commands = None):
        """Basic action constructor

        Args:
            controller: A fife_rpg.ControllerBase instance
            agent: The agent initiating the action
            target: The target of the action
            commands: List of additional commands to execute

        Raises:
            OpenError if the lockable is open.
        """
        Base.__init__(self, controller, agent, target, commands)

    def execute(self):
        description = getattr(self.target, Description.registered_as)
        print "You see %s. \n%s" % (description.view_name, description.desc)
        Base.execute(self)

    @classmethod
    def check_agent(cls, entity): #pylint: disable-msg=W0613
        """Checks whether the entity qualifies as an agent for this action
        
        Args:
            entity: The entity to ceck. A bGrease.Entity instance.

        Returns: True if the entity qualifes. False otherwise
        """
        return True
    
    @classmethod
    def check_target(cls, entity): #pylint: disable-msg=W0613
        """Checks whether the entity qualifies as a target for this action
        
        Args:
            entity: The entity to ceck. A bGrease.Entity instance.

        Returns: True if the entity qualifes. False otherwise
        """
        description = getattr(entity, Description.registered_as)
        if description:
            return True
        return False

    @classmethod
    def register(cls, name="Look"):
        """Registers the class as an action

        Args:
            name: The name under which the class should be registered
            *args: Additional arguments to pass to the class constructor
            **kwargs: Additional keyword arguments to pass to the class 
            constructor

        Returns:
            True if the action was registered, False if not.
        """
        super(LookAction, cls).register(name)