class StopProgram(Exception):
    def __init__(self, account='', status='Stop program'):
        self.account = account
        self.status = status
        self.result = {'account': account, 'status': status}
        super().__init__(status)


def rpc_message_to_error(*args, **kwargs):
    return Exception(*args)


class ReadCancelledError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class TypeNotFoundError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class InvalidChecksumError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class InvalidBufferError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class AuthKeyNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class SecurityError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class CdnFileTamperedError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class AlreadyInConversationError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class BadMessageError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class MultiError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
