class AkamaiError(Exception):
    pass


class AkamaiInvalidRequestParamsException(AkamaiError):
    pass


class AkamaiServiceException(AkamaiError):
    pass


class AkamaiInvalidMethodException(AkamaiError):
    pass


class AkamaiDeleteNotAllowedException(AkamaiError):
    pass


class AkamaiInvalidCpCodeException(AkamaiError):
    pass


class AkamaiResponseMalformedException(AkamaiError):
    pass


class AkamaiInvalidActionException(AkamaiError):
    pass


class AkamaiFileNotFoundException(AkamaiError):
    pass


class AkamaiForbiddenException(AkamaiError):
    pass
