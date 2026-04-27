class VersionControl:
    def __init__(self, config=None, lang=None, log=None):
        self.config = config or {}
        self.lang = lang or {}
        self.log = log
        self.account = None
        self.app_id = None
        self.version = None
        self.android = [
            '11.14.1 (61082)', '11.14.1 (61089)', '11.14.0 (61022)',
            '11.14.0 (61029)', '11.13.4 (60862)', '11.13.4 (60869)',
            '11.13.3 (60812)', '11.13.3 (60819)', '11.13.2 (60602)',
            '11.13.2 (60609)', '11.13.1 (60562)', '11.13.1 (60569)',
        ]
        self.android_x = list(self.android)
        self.desktop = ['5.14.4 x64', '5.14.3 x64', '5.14.2 x64']

    def check(self, account=None, app_id=None, version=None):
        self.account = account
        if isinstance(account, dict):
            self.app_id = account.get('app_id') or account.get('api_id')
            self.version = account.get('app_version')
        if app_id is not None:
            self.app_id = app_id
        if version is not None:
            self.version = version
        return True
