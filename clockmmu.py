from mmu import MMU


class ClockMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for EscMMU
        # pass
        self.frames = frames
        self.memory = {}
        self.page_table = []
        self.pointer = 0
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
            self.memory[page_number][1] = True
            if self.debug:
                print(f"Page {page_number} read from memory.")
        else:
            self.page_faults += 1
            self.replace_page(page_number, 'R')

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        # pass
        if page_number in self.memory:
            self.memory[page_number][0] = 'W'
            self.memory[page_number][1] = True
            if self.debug:
                print(f"Page {page_number} written to memory.")
        else:
            self.page_faults += 1
            self.replace_page(page_number, 'W')
    
    def replace_page(self, page_number, mode):
        if len(self.page_table) < self.frames:
            self.page_table.append(page_number)
            self.memory[page_number] = [mode, True]  # [status, reference bit]
            if self.debug:
                print(f"Page {page_number} loaded into memory.")
        else:
            while True:
                current_page = self.page_table[self.pointer]
                if not self.memory[current_page][1]:  # Reference bit is 0
                    if self.memory[current_page][0] == 'W':  # Write back if dirty
                        self.disk_writes += 1
                        if self.debug:
                            print(f"Page {current_page} written back to disk.")
                    del self.memory[current_page]
                    self.page_table[self.pointer] = page_number
                    self.memory[page_number] = [mode, True]  # [status, reference bit]
                    if self.debug:
                        print(f"Page {current_page} replaced by page {page_number}.")
                    break
                self.memory[current_page][1] = False  # Reset the reference bit to 0
                self.pointer = (self.pointer + 1) % len(self.page_table)  # Circular increment

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
