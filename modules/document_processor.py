"""
Document Processing Module
Author: Emilbek
Last Modified by: Emilbek
Date Last Modified: 04.03.2025
Description: Handles document upload and text extraction from various file formats
Revision History: Initial version 1.0
"""

import os
import PyPDF2
import docx

class DocumentProcessor:
    """
    Processes uploaded documents and extracts plain text
    """
    
    def __init__(self):
        """Initialize the document processor"""
        self.supported_formats = ['txt', 'pdf', 'docx']
        
    def extract_text(self, file_path):
        """
        Extract text from document files
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            str: Extracted text content
        """
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
            
        if file_extension == 'txt':
            return self._extract_from_txt(file_path)
        elif file_extension == 'pdf':
            return self._extract_from_pdf(file_path)
        elif file_extension == 'docx':
            return self._extract_from_docx(file_path)
    
    def _extract_from_txt(self, file_path):
        """Extract text from TXT files"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
            
    def _extract_from_pdf(self, file_path):
        """Extract text from PDF files"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
        return text
        
    def _extract_from_docx(self, file_path):
        """Extract text from DOCX files"""
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])