"""
Text Summarization Tool - Main Application (Simplified)
Author: Emilbek
Last Modified by: Emibek
Date Last Modified: 04.03.2025
Description: Flask web application for text summarization
Revision History: Initial version 1.0
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import time
import io
from werkzeug.utils import secure_filename
import nltk

# Import our modules
from modules.document_processor import DocumentProcessor
from modules.extractive_summarizer import ExtractiveSummarizer
from modules.text_analyzer import TextAnalyzer

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "summarizer_secret_key"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize our modules
document_processor = DocumentProcessor()
extractive_summarizer = ExtractiveSummarizer()
text_analyzer = TextAnalyzer()

# Store the latest summary for download
latest_summary = ""

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    """Handle file upload and summarization"""
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('index'))
    
    if file:
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extract text from file
            text = document_processor.extract_text(file_path)
            
            # Get parameters from form
            summary_length = float(request.form.get('summary_length', 0.3))
            
            # Generate extractive summary
            summary = extractive_summarizer.summarize(text, ratio=summary_length)
            keywords = extractive_summarizer.keyword_extraction(text)
            
            # Analyze text statistics
            text_stats = text_analyzer.analyze_text(text)
            summary_stats = text_analyzer.analyze_text(summary)
            
            # Store summary for download
            global latest_summary
            latest_summary = summary
            
            return render_template('results.html',
                                  original_text=text,
                                  summary=summary,
                                  summary_type="extractive",
                                  text_stats=text_stats,
                                  summary_stats=summary_stats,
                                  keywords=keywords)
                                  
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'danger')
            return redirect(url_for('index'))
        finally:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)

@app.route('/summarize_text', methods=['POST'])
def summarize_text():
    """Handle direct text input and summarization"""
    text = request.form.get('text', '')
    
    if not text:
        flash('No text provided', 'danger')
        return redirect(url_for('index'))
    
    try:
        # Get parameters from form
        summary_length = float(request.form.get('summary_length', 0.3))
        
        # Generate extractive summary
        summary = extractive_summarizer.summarize(text, ratio=summary_length)
        keywords = extractive_summarizer.keyword_extraction(text)
        
        # Analyze text statistics
        text_stats = text_analyzer.analyze_text(text)
        summary_stats = text_analyzer.analyze_text(summary)
        
        # Store summary for download
        global latest_summary
        latest_summary = summary
        
        return render_template('results.html',
                              original_text=text,
                              summary=summary,
                              summary_type="extractive",
                              text_stats=text_stats,
                              summary_stats=summary_stats,
                              keywords=keywords)
                              
    except Exception as e:
        flash(f'Error processing text: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/download/summary')
def download_summary():
    """Download the generated summary as a text file"""
    global latest_summary
    
    if not latest_summary:
        flash('No summary available to download', 'warning')
        return redirect(url_for('index'))
    
    # Create in-memory text file
    buffer = io.BytesIO()
    buffer.write(latest_summary.encode('utf-8'))
    buffer.seek(0)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"summary_{timestamp}.txt"
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )

@app.errorhandler(413)
def too_large(e):
    """Handle file size exceeding limit"""
    flash('File is too large. Maximum file size is 16MB.', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(500)
def server_error(e):
    """Handle server errors"""
    flash('An error occurred while processing your request. Please try again.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)