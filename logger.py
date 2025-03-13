class Logger:
    def __init__(self):
        self._name = "SnipVault"
        self._bold_cyan = "\x1b[36;1m"
        self._white = "\x1b[37;20m"
        self._reset = "\x1b[0m"

    def log(self, msg):
        print("🗂️ " + self._bold_cyan + self._name + self._reset + self._white + ": " + msg)