from transformers import pipeline
import logging
from config import MAX_SUMMARY_LENGTH, MIN_SUMMARY_LENGTH

def summarize_content(content):
    """
    Summarizes the provided content using a free NLP model.
    :param content: Text content to summarize.
    :return: Summarized text.
    """
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(content, max_length=MAX_SUMMARY_LENGTH,
                             min_length=MIN_SUMMARY_LENGTH, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error summarizing content: {e}")
        return f"Error summarizing content. {e}"
