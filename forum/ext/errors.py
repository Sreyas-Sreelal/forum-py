
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