from mmu import MMU

class ClockMMU(MMU):
    def __init__(self, frames):
        self.frames = frames        # Number of frames in memory
        self.memory = {}            # Memory dictionary to store pages
        self.page_table = []        # Page table to keep track of pages in memor
        self.pointer = 0            # Pointer to keep track of the page to replace
        self.disk_reads = 0
        self.disk_writes = 0
        self.page_faults = 0
        self.debug = False

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def read_memory(self, page_number):             
    # If the page is in memory, update its reference bit to True.
    # If not, handle the page fault by replacing a page.

        if page_number in self.memory:              
            self.memory[page_number][1] = True  # Set reference bit to True
            if self.debug:
                print(f"Page {page_number} read from memory.")
        else:
            self.page_faults += 1
            self.replace_page(page_number, 'R')     # Handle page fault and load page

    def write_memory(self, page_number):            
    # If the page is in memory, mark it as dirty ('W') and update its reference bit.
    # If not, handle the page fault by replacing a page.

        if page_number in self.memory:              
            self.memory[page_number][0] = 'W'   # Mark page as written (dirty)
            self.memory[page_number][1] = True  # Set reference bit to True
            if self.debug:
                print(f"Page {page_number} written to memory.")
        else:
            self.page_faults += 1
            self.replace_page(page_number, 'W') # Handle page fault and load page

    def replace_page(self, page_number, mode):          
    # If there's an empty frame, load the new page directly.
    # If memory is full, find a page with a reference bit of 0 to replace.

        if len(self.page_table) < self.frames:          # Memory has space, so load the page into the next available slot.          
            self.page_table.append(page_number)
            self.memory[page_number] = [mode, True]     # Set page mode and reference bit
            if self.debug:
                print(f"Page {page_number} loaded into memory.")
        else:                                           # Memory is full, so find a page to replace using the Clock algorithm.
            while True:
                current_page = self.page_table[self.pointer]
                if not self.memory[current_page][1]:            # Reference bit is 0
                    if self.memory[current_page][0] == 'W':     # Write back if dirty
                        self.disk_writes += 1
                        if self.debug:
                            print(f"Page {current_page} written back to disk.")
                    del self.memory[current_page]                   # Remove the old page
                    self.page_table[self.pointer] = page_number     # Replace it with the new page
                    self.memory[page_number] = [mode, True]         # Set new page mode and reference bit
                    if self.debug:
                        print(f"Page {current_page} replaced by page {page_number}.")
                    self.pointer = (self.pointer + 1) % len(self.page_table)    # Move pointer to the next page
                    break
                self.memory[current_page][1] = False    # If reference bit is 1, reset it and move pointer to the next page.
                self.pointer = (self.pointer + 1) % len(self.page_table)

        self.disk_reads += 1     # A new page is loaded from the disk, so increment the disk read counter.

    def get_total_disk_reads(self):
        return self.disk_reads

    def get_total_disk_writes(self):
        return self.disk_writes

    def get_total_page_faults(self):
        return self.page_faults
