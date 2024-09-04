from mmu import MMU


class ClockMMU(MMU):
    def __init__(self, frames):
        self.frames = frames    # Number of frames in memory
        self.memory = {}        # Memory dictionary to store pages
        self.page_table = []    # Page table to keep track of pages in memory
        self.pointer = 0        # Pointer to keep track of the page to replace
        self.disk_reads = 0     # Number of disk reads
        self.disk_writes = 0    # Number of disk writes
        self.page_faults = 0    # Number of page faults
        self.debug = False      # Debug flag

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number):
        if self.debug:
            print(f"Page number: {page_number}")
            print(f"Mode: R")
            print()

        if page_number in self.memory:  # Page is in memory 
            self.memory[page_number][1] = True 
            if self.debug:
                print(f"Page {page_number} read from memory.")
        else:   # Page is not in memory
            self.page_faults += 1
            self.replace_page(page_number, 'R')
        
        if self.debug:
            print(f"Memory: {self.memory}")
            print(f"Page table: {self.page_table}")
            print(f"Pointer: {self.pointer}")
            print(f"Disk reads: {self.disk_reads}")
            print(f"Disk writes: {self.disk_writes}")
            print(f"Page faults: {self.page_faults}")
            print()

    def write_memory(self, page_number):
        if self.debug:
            print(f"Page number: {page_number}")
            print(f"Mode: W")
            print()

        if page_number in self.memory:  # Page is in memory
            self.memory[page_number][0] = 'W'
            self.memory[page_number][1] = True 
            if self.debug:
                print(f"Page {page_number} written to memory.")
        else:   # Page is not in memory
            self.page_faults += 1
            self.replace_page(page_number, 'W')

        if self.debug:
            print(f"Memory: {self.memory}")
            print(f"Page table: {self.page_table}")
            print(f"Pointer: {self.pointer}")
            print(f"Disk reads: {self.disk_reads}")
            print(f"Disk writes: {self.disk_writes}")
            print(f"Page faults: {self.page_faults}")
            print()

    
    def replace_page(self, page_number, mode):
        if len(self.page_table) < self.frames:  # Memory is not full 
            self.page_table.append(page_number)
            self.memory[page_number] = [mode, True]  # [status, reference bit]
            if self.debug:
                print(f"Page {page_number} loaded into memory.")
        else:   # Memory is full 
            while True:
                current_page = self.page_table[self.pointer]
                if not self.memory[current_page][1]:  # Reference bit is 0
                    if self.memory[current_page][0] == 'W':  # Write back if dirty
                        self.disk_writes += 1
                        if self.debug:
                            print(f"Page {current_page} written back to disk.")
                    del self.memory[current_page]   # Remove the page from memory
                    self.page_table[self.pointer] = page_number # Replace the page in the page table
                    self.memory[page_number] = [mode, True]  # [status, reference bit]
                    if self.debug:
                        print(f"Page {current_page} replaced by page {page_number}.")
                    break
                self.memory[current_page][1] = False  # Reset the reference bit to 0
                self.pointer = (self.pointer + 1) % len(self.page_table) # Move the pointer to the next page

        self.disk_reads += 1 # Read from disk

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
