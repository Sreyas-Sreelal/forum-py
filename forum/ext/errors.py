# -*- coding: utf-8 -*-
"""
Copyright (C) 2018  Sreyas Sreelal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

class Error(Exception):
    pass

class InvalidCreditinals(Error):
    """
    Raised when creditinals provided is wrong
    """
    pass

class DriverLoadError(Error):
    """
    Raised when phantom JS driver is not found
    """
    pass

class MaxLoginLimit(Error):
    """
    Raised when forum login limit is reached (wait for 15 minutes before attempting another login)
    """
    pass

class MustLogin(Error):
    """
    Raised when a non-logged in attempt to process a request that needs a logged in account
    """
    pass

class InvalidUserId(Error):
    """
    Raised when invalid user id is specified
    """
    pass

class InvalidThreadId(Error):
    """
    Raised when invalid thread id is specified
    """
    pass

class RecipentLimitReached(Error):
    """
    Raised when more than 5 number of recipents is used in the pm
    """
    pass

class MaxPMLimit(Error):
    """
    Raised when forum pm limit is reached (wait for 60 seconds before sending another pm)
    """
    pass



