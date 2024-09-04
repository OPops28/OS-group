from mmu import MMU
import random

class RandMMU(MMU):
    def __init__(self, frames):
        self.frames = frames    # Number of frames in memory
        self.memory = {}        # Memory dictionary to store pages
        self.page_table = []    # Page table to keep track of pages in memory
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number):
    # If the page is in memory, do nothing.
    # If not, handle the page fault by randomly replacing an existing page.

        if page_number in self.memory:
            if self.debug:
                print(f"Page {page_number} read from memory.")
        else:
            self.page_faults += 1
            if len(self.page_table) < self.frames:          # Memory has space, so load the page into the next available slot.
                self.page_table.append(page_number)
            else:
                victim = random.choice(self.page_table)     # Memory is full, so randomly replace a page in memory.
                self.page_table.remove(victim)
                if self.memory[victim] == 'W':              # Write back if the victim page is dirty
                    self.disk_writes += 1
                self.page_table.append(page_number)
                if self.debug:
                    print(f"Page {victim} replaced by page {page_number}.")
                del self.memory[victim]                     # Remove the old page from memory
            self.memory[page_number] = 'R'                  # Load the new page with read status
            self.disk_reads += 1
            if self.debug:
                print(f"Page {page_number} loaded into memory.")

    def write_memory(self, page_number):
    # If the page is in memory, mark it as dirty.
    # If not, handle the page fault by randomly replacing an existing page.

        if page_number in self.memory:
            self.memory[page_number] = 'W'      # Mark page as written (dirty)
            if self.debug:
                print(f"Page {page_number} written to memory.")
        else:
            self.page_faults += 1
            if len(self.page_table) < self.frames:      # Memory has space, so load the page into the next available slot.
                self.page_table.append(page_number)
            else:
                victim = random.choice(self.page_table) # Memory is full, so randomly replace a page in memory.
                self.page_table.remove(victim)
                if self.memory[victim] == 'W':          # Write back if the victim page is dirty
                    self.disk_writes += 1
                if self.debug:
                    print(f"Page {victim} replaced by page {page_number}.")
                del self.memory[victim]                 # Remove the old page from memory
            self.memory[page_number] = 'W'              # Load the new page with write status
            self.disk_reads += 1
            if self.debug:
                print(f"Page {page_number} loaded into memory.")

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
