import os
import unittest

from langchain_core.prompts import BasePromptTemplate
from prompts.prompt_loader import load_prompt


class TestLoadPrompt(unittest.TestCase):
    def setUp(self):
        # 테스트를 위한 YAML 파일 생성
        self.test_yaml_content = """
        _type: "prompt"
        template: |
            당신은 친절한 AI 어시스턴트 입니다. 사용자의 요청사항에 따라 적절한 답변을 작성해 주세요.
  
            #Question:
            {question}

            #Answer:
            input_variables: ["question"]
        """
        self.test_file_path = "test_prompt.yaml"
        with open(self.test_file_path, "w", encoding="utf8") as f:
            f.write(self.test_yaml_content)

    def tearDown(self):
        # 테스트 파일 정리
        os.remove(self.test_file_path)

    def test_load_prompt(self):
        # 함수 테스트
        prompt_template = load_prompt(self.test_file_path)

        # 타입 체크
        self.assertIsInstance(prompt_template, BasePromptTemplate)

        # 입력 변수 체크
        self.assertEqual(set(prompt_template.input_variables), {"question"})

        # 포맷 결과 체크
        result = prompt_template.format(question="SALMON")
        self.assertIn("#Question:\nSALMON", result)


if __name__ == '__main__':
    unittest.main()