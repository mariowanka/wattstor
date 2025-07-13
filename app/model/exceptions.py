class ModelException(Exception):
    pass


class WrongDeviceTypeException(ModelException):
    message = "Unknown device type"
