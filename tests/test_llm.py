import unittest
from deepsearcher.llm.base import BaseLLM, ChatResponse

class TestLLMBase(unittest.TestCase):
    def test_r1_tag_handling(self):
        """Test that <think> tags are properly stripped from responses."""
        response = "<think>This is a thought process.</think>Final answer"
        result = BaseLLM.literal_eval(response)
        self.assertEqual(result, "Final answer")

    def test_r1_tag_handling_with_code(self):
        """Test that <think> tags are stripped and code blocks are properly parsed."""
        response = "<think>Analyzing...</think>```python\n['query1', 'query2']```"
        result = BaseLLM.literal_eval(response)
        self.assertEqual(result, ['query1', 'query2'])
