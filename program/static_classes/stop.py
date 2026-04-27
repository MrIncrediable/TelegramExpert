class _StopBase(Exception):
    default_status = ''

    def __init__(self, account='', status=None):
        status = self.default_status if status is None else status
        self.account = account
        self.status = status
        self.result = {'account': account, 'status': status}
        super().__init__(status)


class PeerFlood(_StopBase):
    default_status = 'Account is limited'


class MaxFlood(_StopBase):
    default_status = 'Max flood reached'


class BanAccount(_StopBase):
    default_status = 'Account is banned'


class StopAccount(_StopBase):
    default_status = 'Account stopped'


class AutoStopCheck:
    def __init__(self, stop_thread=None):
        self.stop_thread = stop_thread

    def check(self):
        return bool(self.stop_thread and self.stop_thread.is_set())


class AutoStop(AutoStopCheck):
    def __call__(self):
        if self.check():
            raise StopAccount(status='Stopped')
        return False
