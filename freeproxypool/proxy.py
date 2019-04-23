class Proxy():
    def __init__(self):
        self.status = 'new'
        self.total_ok_count = 0
        self.total_fail_count = 0
        self.continuous_fail_count = 0
        self.check_record = []
