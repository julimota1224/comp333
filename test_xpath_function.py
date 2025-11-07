import unittest
from files.download_eep import test_xpath_index  # Fixed import

class TestXPathCalculation(unittest.TestCase):
    """Unit tests for the test_xpath_index function."""
    
    def test_vcrit_a_first_metallicity(self):
        """Test v/vcrit=0.4 with first [Fe/H] option."""
        self.assertEqual(test_xpath_index('A', 1), 54)
    
    def test_vcrit_a_middle_metallicity(self):
        """Test v/vcrit=0.4 with middle [Fe/H] option."""
        self.assertEqual(test_xpath_index('A', 8), 61)
    
    def test_vcrit_a_last_metallicity(self):
        """Test v/vcrit=0.4 with last [Fe/H] option."""
        self.assertEqual(test_xpath_index('A', 15), 68)
    
    def test_vcrit_b_first_metallicity(self):
        """Test v/vcrit=0.0 with first [Fe/H] option."""
        self.assertEqual(test_xpath_index('B', 1), 69)
    
    def test_vcrit_b_middle_metallicity(self):
        """Test v/vcrit=0.0 with middle [Fe/H] option."""
        self.assertEqual(test_xpath_index('B', 8), 76)
    
    def test_vcrit_b_last_metallicity(self):
        """Test v/vcrit=0.0 with last [Fe/H] option."""
        self.assertEqual(test_xpath_index('B', 16), 84)  # Fixed: 16 not 15
    
    def test_invalid_vcrit_choice(self):
        """Test invalid v/vcrit choice raises error."""
        with self.assertRaises(ValueError):
            test_xpath_index('C', 1)
    
    def test_invalid_metallicity_too_low(self):
        """Test metallicity index too low raises error."""
        with self.assertRaises(ValueError):
            test_xpath_index('A', 0)
    
    def test_invalid_metallicity_type(self):
        """Test non-integer metallicity raises error."""
        with self.assertRaises(ValueError):
            test_xpath_index('A', '5')

if __name__ == '__main__':
    unittest.main()