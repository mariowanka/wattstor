class ModelException(Exception):
    pass


class WrongDeviceTypeException(ModelException):
    message = "Unknown device type"


class UserExistsException(ModelException):
    message = "Given user already exists"


class WrongAuthenticationException(ModelException):
    message = "Wrong given user or password"
