from mmu import MMU
from collections import OrderedDict

class LruMMU(MMU):
    def __init__(self, frames):
        self.frames = frames            # Number of frames in memory
        self.memory = OrderedDict()     # Memory dictionary to store pages in order of access
        self.disk_reads = 0             # Number of disk reads
        self.disk_writes = 0            # Number of disk writes 
        self.page_faults = 0            # Number of page faults
        self.debug = False              # Debug flag

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number):
        if page_number in self.memory:
            self.memory.move_to_end(page_number)
            if self.debug:
                print(f"Page {page_number} read from memory.")
        else:
            self.page_faults += 1
            if len(self.memory) >= self.frames:
                victim, status = self.memory.popitem(last=False)
                if status == 'W':
                    self.disk_writes += 1
                if self.debug:
                    print(f"Page {victim} replaced by page {page_number}.")
            self.memory[page_number] = 'R'
            self.disk_reads += 1

    def write_memory(self, page_number):
        if page_number in self.memory:
            self.memory[page_number] = 'W'
            self.memory.move_to_end(page_number)
            if self.debug:
                print(f"Page {page_number} written to memory.")
        else:
            self.page_faults += 1
            if len(self.memory) >= self.frames:
                victim, status = self.memory.popitem(last=False)
                if status == 'W':
                    self.disk_writes += 1
                if self.debug:
                    print(f"Page {victim} replaced by page {page_number}.")
            self.memory[page_number] = 'W'
            self.disk_reads += 1

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
