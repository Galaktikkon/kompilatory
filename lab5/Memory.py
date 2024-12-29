

class Memory:
    def __init__(self, name): # memory name
        self.name = name
        self.heap = {}

    def has_key(self, name):  # variable name
        return name in self.heap
    
    def get(self, name):         # gets from memory current value of variable <name>
        return self.heap.get(name, None)
    
    def put(self, name, value):  # puts into memory current value of variable <name>
        self.heap.update({name: value})

class MemoryStack:                                                      
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        memory = Memory('global') if memory is None else memory
        self.stack = [memory]

    def get(self, name):             # gets from memory stack current value of variable <name>
        for element in reversed(self.stack):
            value = element.get(name)
            if value is not None:
                return value
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for element in reversed(self.stack):
            if element.has_key(name):
                element.put(name, value)
                return
        self.insert(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()

