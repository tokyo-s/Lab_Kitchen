from .config import *


class Kitchen:
    def __init__(self, nr_cooks=NR_COOKS, nr_ovens=NR_OVENS, nr_stoves=NR_STOVES):
        self.nr_cooks = nr_cooks
        self.nr_ovens = nr_ovens
        self.nr_stoves = nr_stoves

    def run_test(self):
        pass
