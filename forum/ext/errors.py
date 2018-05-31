
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

    