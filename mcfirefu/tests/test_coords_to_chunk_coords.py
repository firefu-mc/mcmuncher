import unittest
import mcfirefu.coord_utils

# These were manually verified using
# https://minecraft.tools/en/coordinate-calculator.php
# [block_coordinate, chunk_coordinate]
coords = [
    [0,0],
    [1,0],
    [15,0],
    [16,1],
    [50,3],
    [991,61],
    [1007,62],
    [1008,63],
    [100000,6250],
    [-1,-1],
    [-16,-1],
    [-17,-2],
    [-50,-4],
    [-992,-62],
    [-993,-63],
    [-1008,-63],
    [-1009,-64],
    [-100000,-6250],
]

class TestCoordsToChunkCoords(unittest.TestCase):
    def test_convert_coords_to_chunk_coords(self):
        for pair in coords:
            print(pair)
            chunk = mcfirefu.coord_utils.convert_coords_to_chunk_coords([pair[0], pair[0]])
            self.assertEqual(chunk, [pair[1],pair[1]])

if __name__ == '__main__':
    unittest.main()
