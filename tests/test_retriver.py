import os
import unittest

from fpdf import FPDF

from retriver import create_retriever


class TestRetriever(unittest.TestCase):

    def setUp(self):
        self.file_path = "test.pdf"
        self.create_sample_pdf()

    def tearDown(self):
        os.remove(self.file_path)


    def create_sample_pdf(self):
        """
        샘플 PDF 파일을 생성하는 함수입니다.
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="This is for test Document", ln=True)
        pdf.cell(200, 10, txt="KO Group's financial and security affiliate INITECH held an extraordinary shareholders' meeting on the 18th and announced on the 22nd that it appointed Vice President Hong Gil-dong as its new CEO.", ln=True)

        pdf.output(self.file_path)

    def test_create_retriever(self):

        retriever = create_retriever(self.file_path)

        # 관련 있는 단어 검색
        query_result = retriever.get_relevant_documents("CEO")
        self.assertGreater(len(query_result), 0, "연관성 있는 단어에 대한 검색 결과 확인")

        # 관련 없는 단어 검색
        # empty_query_result = retriever.get_relevant_documents("")
        # self.assertEqual(len(empty_query_result), 0, "빈 쿼리에 대한 검색 결과가 비어 있음")

if __name__ == '__main__':
    unittest.main()