from googletrans import Translator

def translate_po_file(input_file, output_file, dest_lang):
    translator = Translator()
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    translated_lines = []
    for line in lines:
        if line.startswith('msgid "') and 'msgstr' not in line:
            original_text = line[7:-2]  # Extract text
            translation = translator.translate(original_text, dest=dest_lang).text
            translated_lines.append(line)  # Keep original msgid
            translated_lines.append(f'msgstr "{translation}"\n')
        else:
            translated_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)

# Example usage
translate_po_file("locale/fr/LC_MESSAGES/django.po", "locale/fr/LC_MESSAGES/django.po", "fr")


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Translate your text or database fields."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Translation script executed successfully!'))
