import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import re

# NLTK verilerini indir
nltk.download('punkt', quiet=True)


def preprocess_text(text):
    """Metni ön işleme: Fazla boşlukları kaldır, özel karakterleri temizle"""
    text = re.sub(r'\s+', ' ', text)  # Fazla boşlukları kaldır
    text = text.strip()
    return text


def summarize_text(text, ratio=0.3, algorithm="text_rank"):
    """
    Metni özetler
    """
    try:
        # Metni ön işle
        text = preprocess_text(text)

        # Çok kısa metinler için
        if len(text.split()) < 30:
            return text

        # Sumy ile özetleme
        parser = PlaintextParser.from_string(text, Tokenizer("english"))

        if algorithm == "text_rank":
            summarizer = TextRankSummarizer()
        elif algorithm == "lsa":
            stemmer = Stemmer("english")
            summarizer = LsaSummarizer(stemmer)
        elif algorithm == "lex_rank":
            summarizer = LexRankSummarizer()
        else:
            summarizer = TextRankSummarizer()

        summarizer.stop_words = get_stop_words("english")

        # Özet cümle sayısını hesapla
        sentences = parser.document.sentences
        sentence_count = max(1, min(5, int(len(sentences) * ratio)))

        # En az 2, en fazla 5 cümle olsun
        sentence_count = max(2, min(5, sentence_count))

        # Özetleme yap
        summary_sentences = summarizer(parser.document, sentence_count)
        summary = " ".join(str(sentence) for sentence in summary_sentences)

        # Özet çok kısa çıkarsa veya hiç çıkmazsa yedek özetleme kullan
        if len(summary.strip()) < 20 or not summary:
            return backup_summarize(text)

        return summary

    except Exception as e:
        # Hata durumunda yedek özetleme
        return backup_summarize(text)


def backup_summarize(text):
    """TextRank başarısız olursa kullanılacak yedek özetleme"""
    try:
        # Önce LSA dene
        text = preprocess_text(text)
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        stemmer = Stemmer("english")
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")

        sentences = parser.document.sentences
        sentence_count = max(2, min(5, int(len(sentences) * 0.3)))

        summary_sentences = summarizer(parser.document, sentence_count)
        summary = " ".join(str(sentence) for sentence in summary_sentences)

        if len(summary.strip()) > 20:
            return summary

        # LSA da başarısız olursa basit özetleme kullan
        return simple_summarize(text)

    except Exception as e:
        return simple_summarize(text)


def simple_summarize(text):
    """Basit kural tabanlı yedek özetleme"""
    sentences = nltk.sent_tokenize(text)

    if len(sentences) <= 2:
        return text

    # Metnin ilk ve son cümlelerini al (genellikle önemli bilgiler içerirler)
    if len(sentences) > 4:
        # İlk 2 ve son 1 cümleyi al
        return ' '.join(sentences[:2] + [sentences[-1]])
    elif len(sentences) > 2:
        # İlk ve son cümleyi al
        return ' '.join([sentences[0], sentences[-1]])

    return ' '.join(sentences[:3])