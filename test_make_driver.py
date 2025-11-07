import unittest
from files.download_eep import make_driver

class TestMakeDriver(unittest.TestCase):
    """Unit tests for the make_driver function."""
    
    def test_returns_driver_object(self):
        """Test that function returns a driver object."""
        driver = make_driver()
        self.assertIsNotNone(driver)
        driver.quit()
    
    def test_driver_can_quit(self):
        """Test that driver can be closed."""
        driver = make_driver()
        try:
            driver.quit()
        except Exception as e:
            self.fail(f"driver.quit() raised {e}")

if __name__ == '__main__':
    unittest.main()