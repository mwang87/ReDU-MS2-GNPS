import unittest
import sys
import ccmsproteosafepythonapi
sys.path.insert(1,'../')
import redu_pca 

class TestFunctions(unittest.TestCase):    
    def test_redu_pca(self):
        redu_pca.project_new_data("./reference_data/f39c94cb7afe4568950bf61cdb8fee0d.txt", "./tempuploads", calculate_neighbors=False, unit_test=True)
        redu_pca.project_new_data("./reference_data/f39c94cb7afe4568950bf61cdb8fee0d.txt", "./tempuploads", calculate_neighbors=True, unit_test=True)
    
   #TODO
   #@unittest.expectedFailure
   #def test_redu_pca_fail(self): 

if __name__ == "__main__":
    unittest.main()
