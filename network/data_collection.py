class Data_Collection():

    def __init__():

        self.path = ""
        self.imsc = ""
        self.scan = ""
        self.loop = 0
        self.glob = 0

    def set_data_field(self, data):
        ''' 
        Chooses which field the info should be adssigned to.
        field: a string representing the field (example: "PATH", "IMSC", etc.)
        '''

        if "PATH" in data:
            self.path = data[5:]
            return 1
        
        elif "IMSC" in data:
            self.imsc = int(data[5:])
            return 1
        
        elif "SCAN" in data:
            self.scan = int(data[5:])
            return 1
        
        elif "LOOP" in data:
            self.loop = int(data[5:])
            return 1
        
        elif "GLOB" in data:
            self.glob = int(data[5:])
            return 1
        
        else:
            print("Field Not recognized. Check spelling!")
            return 0
        
