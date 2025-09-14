from app.summarizer import summarize_text


test_text = """
Artificial intelligence is increasingly becoming a part of daily life. Smart assistants like Siri and Alexa help users manage tasks, set reminders, and answer questions. AI-driven recommendation systems on platforms like Netflix and YouTube suggest content based on user preferences. In the automotive industry, autonomous driving technology is being developed to increase road safety and reduce human error. AI also plays a significant role in healthcare by assisting in medical imaging analysis, predicting patient outcomes, and supporting personalized treatment plans. Despite these benefits, AI raises concerns about privacy, job automation, and ethical use of data. Researchers continue to explore ways to make AI more transparent, fair, and accountable while expanding its applications across different sectors.
"""

print("Original text length:", len(test_text))
print("Word count:", len(test_text.split()))

# Farklı algoritmaları test et
algorithms = ["text_rank", "lsa", "lex_rank"]

for algo in algorithms:
    summary = summarize_text(test_text, algorithm=algo)
    print(f"\n--- {algo.upper()} ---")
    print("Summary length:", len(summary))
    print("Summary:", summary)




