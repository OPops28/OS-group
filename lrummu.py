from mmu import MMU
from collections import OrderedDict

class LruMMU(MMU):
    def __init__(self, frames):
        self.frames = frames            # Number of frames in memory
        self.memory = OrderedDict()     # Memory dictionary to store pages in order of access
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number):
    # If the page is in memory, move it to the end to mark it as recently used.
    # If not, handle the page fault by replacing the least recently used page.
 
        if page_number in self.memory:                   
            self.memory.move_to_end(page_number)            # Mark page as recently used
            if self.debug:
                print(f"Page {page_number} read from memory.")
        else:
            self.page_faults += 1
            if len(self.memory) >= self.frames:                  # Memory is full, so replace the least recently used page (first item in OrderedDict).
                victim, status = self.memory.popitem(last=False)
                if status == 'W':                                # Write back if the victim page is dirty
                    self.disk_writes += 1
                if self.debug:
                    print(f"Page {victim} replaced by page {page_number}.")
            self.memory[page_number] = 'R'                       # Load the new page with read status
            self.disk_reads += 1
            if self.debug:
                print(f"Page {page_number} loaded into memory.")

    def write_memory(self, page_number):
    # If the page is in memory, mark it as dirty and move it to the end to mark it as recently used.
    # If not, handle the page fault by replacing the least recently used page.

        if page_number in self.memory:
            self.memory[page_number] = 'W'          # Mark page as written (dirty)
            self.memory.move_to_end(page_number)    # Mark page as recently used
            if self.debug:
                print(f"Page {page_number} written to memory.")
        else:
            self.page_faults += 1
            if len(self.memory) >= self.frames:          # Memory is full, so replace the least recently used page.
                victim, status = self.memory.popitem(last=False)
                if status == 'W':                        # Write back if the victim page is dirty
                    self.disk_writes += 1
                if self.debug:
                    print(f"Page {victim} replaced by page {page_number}.")
            self.memory[page_number] = 'W'               # Load the new page with write status
            self.disk_reads += 1
            if self.debug:
                print(f"Page {page_number} loaded into memory.")

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
