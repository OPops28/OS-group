from mmu import MMU
import random

class RandMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU
        # pass
        self.frames = frames
        self.memory = {}
        self.page_table = []
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        # pass
        self.debug = True

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        # pass
        self.debug = False

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        # pass
        if page_number in self.memory:
            if self.debug:
                print(f"Page {page_number} read from memory.")
        else:
            self.page_faults += 1
            if len(self.page_table) < self.frames:
                self.page_table.append(page_number)
            else:
                victim = random.choice(self.page_table)
                self.page_table.remove(victim)
                self.page_table.append(page_number)
                if self.debug:
                    print(f"Page {victim} replaced by page {page_number}.")
            self.memory[page_number] = 'R'
            self.disk_reads += 1

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        # pass
        if page_number in self.memory:
            self.memory[page_number] = 'W'
            if self.debug:
                print(f"Page {page_number} written to memory.")
        else:
            self.page_faults += 1
            if len(self.page_table) < self.frames:
                self.page_table.append(page_number)
            else:
                victim = random.choice(self.page_table)
                self.page_table.remove(victim)
                if self.memory[victim] == 'W':
                    self.disk_writes += 1
                self.page_table.append(page_number)
                if self.debug:
                    print(f"Page {victim} replaced by page {page_number}.")
            self.memory[page_number] = 'W'
            self.disk_reads += 1

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        # return -1
        return self.disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        # return -1
        return self.disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        # return -1
        return self.page_faults
