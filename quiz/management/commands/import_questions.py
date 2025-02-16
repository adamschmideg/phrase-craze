import csv
import string
from django.core.management.base import BaseCommand
from quiz.models import Question

class Command(BaseCommand):
    help = 'Import data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            objects_to_create = []
            for row in reader:
                s = row['sentence']
                while s and s[-1] in string.punctuation:
                    s = s[:-1]
                words = s.split()
                objects_to_create.append(
                    Question(
                        text=s,
                        difficulty=len(words),
                    ))

            Question.objects.bulk_create(objects_to_create)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
