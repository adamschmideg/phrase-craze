import spacy
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from quiz.models import Question, Answer  # Adjust the import based on your actual app structure
import wn
wn.download('omw-nl:1.4')
dutch_wn = wn.Wordnet('omw-nl:1.4')

def get_dutch_synonyms(word):
    synonyms = set()
    synsets = dutch_wn.synsets(word)

    for synset in synsets:
        for lemma in synset.lemmas():
            if lemma != word:  # Avoid adding the input word itself
                synonyms.add(lemma)

    return list(synonyms)

word = "man"
print(f"Synonyms for '{word}': {get_dutch_synonyms(word)}")

# Load Dutch language model
nlp = spacy.load("nl_core_news_sm")

# List of common Dutch adverbs
dutch_adverbs = [
    "snel", "langzaam", "vaak", "altijd", "nooit",
    "soms", "eerder", "later", "misschien", "zeker",
    "heel", "erg", "behoorlijk", "totaal", "absoluut",
    "slechts", "gewoon", "ook", "daar", "hier",
    "verder", "dichtbij", "ver weg", "samen", "apart",
    "alleen", "dus", "echter", "bovendien", "daarom"
]

class Command(BaseCommand):
    help = 'Generate near-match answers for questions without answers'

    def handle(self, *args, **options):
        batch_size = 100  # Number of questions to process at a time
        questions = Question.objects.filter(answers__isnull=True)

        for i in range(0, len(questions), batch_size):
            batch_questions = questions[i:i + batch_size]
            self.stdout.write(f'Processing batch {i // batch_size + 1}...')
            bulk_answers = []

            for question in batch_questions:
                sentence_length = len(question.text.split())

                for length in range(3, sentence_length - 1):
                    alternative_answers_count = 5
                    for _ in range(alternative_answers_count):
                        subsentence = self.random_subsentence(question.text, length)
                        near_match = self.create_near_match(subsentence)
                        sub_length = len(near_match.split())
                        bulk_answers.append(Answer(question=question, text=near_match, difficulty=sub_length))  # Create new answer

                    subsentence = self.random_subsentence(question.text, length)
                    bulk_answers.append(Answer(question=question, text=subsentence, is_correct=True, difficulty=length))  # Create correct answer

            Answer.objects.bulk_create(bulk_answers)

    def random_subsentence(self, sentence, length):
        doc = nlp(sentence)
        words = [token.text for token in doc]
        start = random.randint(0, len(words) - length)
        return ' '.join(words[start:start + length])

    def create_near_match(self, sentence):
        doc = nlp(sentence)

        words = [token.text for token in doc]
        original_words = words.copy()  # Keep a copy of the original words

        technique = random.choice(["substitute", "reorder", "add_remove"])

        if technique == "substitute":
            for i, token in enumerate(doc):
                if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV']:
                    synonyms = get_dutch_synonyms(token.text)
                    if synonyms:
                        new_word = random.choice(synonyms)
                        if new_word != token.text:
                            words[i] = new_word
                            break

        elif technique == "reorder":
            if len(words) > 3:
                i, j = random.sample(range(len(words)), 2)
                words[i], words[j] = words[j], words[i]

        else:  # add_remove
            if random.choice([True, False]) and len(words) > 4:
                removable = [i for i, t in enumerate(doc) if t.dep_ not in ['ROOT', 'nsubj', 'aux']]
                if removable:
                    words.pop(random.choice(removable))
            else:
                insert_pos = random.randint(0, len(words))
                adverb_to_insert = random.choice(dutch_adverbs)
                words.insert(insert_pos, adverb_to_insert)

        near_match = ' '.join(words)

        # Ensure the near match is different from the original sentence
        if near_match.lower() == sentence.lower():
            if len(words) > 3:
                i, j = random.sample(range(len(words)), 2)
                words[i], words[j] = words[j], words[i]
            else:
                insert_pos = random.randint(0, len(words))
                adverb_to_insert = random.choice(dutch_adverbs)
                words.insert(insert_pos, adverb_to_insert)

            near_match = ' '.join(words)

        near_match = near_match[0].upper() + near_match[1:]  # Capitalize first letter

        return near_match

