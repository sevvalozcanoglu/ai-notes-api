# test_summarizer.py
import sys
import os

# Proje yolunu ekleyin
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app.summarizer import summarize_text

# Test metni
test_text = """
Artificial intelligence is transforming industries across the globe, from healthcare to finance, transportation, and education. Machine learning algorithms can analyze vast amounts of data to detect patterns, make predictions, and automate decision-making processes. Natural language processing enables computers to understand and interact using human language, while computer vision allows machines to interpret images and videos. These technologies are increasingly integrated into everyday applications such as virtual assistants, autonomous vehicles, fraud detection systems, and personalized recommendation engines. The rapid pace of AI development brings both opportunities and challenges, including ethical considerations, job displacement, and the need for robust regulatory frameworks
"""

# Özetleme yap
summary = summarize_text(test_text)
print("Orijinal metin uzunluğu:", len(test_text))
print("Özet uzunluğu:", len(summary))
print("Özet:", summary)




