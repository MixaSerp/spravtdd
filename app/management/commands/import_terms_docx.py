import re
from django.core.management.base import BaseCommand
from docx import Document
from app.models import Term

class Command(BaseCommand):
    help = 'Импорт терминов из DOCX файла'

    def add_arguments(self, parser):
        parser.add_argument('docx_file', type=str, help='Путь к DOCX файлу')

    def handle(self, *args, **options):
        docx_file = options['docx_file']
        success_count = 0
        error_count = 0

        try:
            doc = Document(docx_file)
            terms = []
            current_term = None
            current_definition = []

            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                
                if not text:
                    continue
                
                if re.match(r'^[А-ЯЁ]$', text):
                    continue
                
                match = re.match(r'^([А-Яа-яЁёA-Za-z0-9\-\s]+(?:\([^)]+\))?)\s*[—-]\s*(.+)$', text)
                
                if match:
                    if current_term:
                        terms.append({
                            'name': current_term,
                            'definition': ' '.join(current_definition).strip()
                        })
                    
                    current_term = match.group(1).strip()
                    current_definition = [match.group(2).strip()]
                else:

                    if current_term:
                        current_definition.append(text)

            if current_term:
                terms.append({
                    'name': current_term,
                    'definition': ' '.join(current_definition).strip()
                })

            for term_data in terms:
                try:
                    if term_data['name'] and term_data['definition']:
                        term, created = Term.objects.update_or_create(
                            name=term_data['name'],
                            defaults={
                                'definition': term_data['definition'],
                            }
                        )
                        success_count += 1
                        status = "Создан" if created else "Обновлён"
                        self.stdout.write(self.style.SUCCESS(f'{status}: {term_data["name"][:60]}'))
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f'Ошибка: {term_data.get("name", "N/A")} - {str(e)}'))

            self.stdout.write(self.style.SUCCESS(
                f'\nУспешно: {success_count}, Ошибок: {error_count}'
            ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл не найден: {docx_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {str(e)}'))