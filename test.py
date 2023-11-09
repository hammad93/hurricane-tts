import unittest
import prompts

class TestPrompts(unittest.TestCase):
    error_msg = "My function raised an exception {e}"
    def test_prompt_generation(self):
        try:
            prompts.generate_prompts()
        except Exception as e:
            self.fail(self.error_msg.format(e=e))
    def test_chat(self):
        try:
            prompts.chat("test")
        except Exception as e:
            self.fail(self.error_msg.format(e=e))

# This allows the test suite to be run from the command line
if __name__ == '__main__':
    unittest.main()