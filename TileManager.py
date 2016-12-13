class TileManager():
    
    def __init__(self, width, height, nw_tile, nh_tile):  # Define and Set width, height of tile
        self.width = width  # width of frame
        self.height = height  # height of frame
        self.nw_tile = nw_tile  # number of tile in x
        self.nh_tile = nh_tile  # number of tile in y
        self.sizew_tile = self.width / self.nw_tile     # width of tile
        self.sizeh_tile = self.height / self.nh_tile    # height of tile
    
    def get_wframe(self):
        return self.width
    
    def get_hframe(self):
        return self.height
        
    def get_nw_tile(self):  # Get nunber of tile (width)
        return self.nw_tile
    
    def get_nh_tile(self):  # Get nunber of tile (height)
        return self.nh_tile
    
    def get_sizew_tile(self):  # Get width of tile
        return self.sizew_tile
    
    def get_sizeh_tile(self):  # Get height of tile
        return self.sizeh_tile
    