import re
import os

locales = ['es', 'fr', 'ru', 'uz']

for locale in locales:
    filepath = f'locale/{locale}/LC_MESSAGES/django.po'
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        result = []
        last_was_msgstr = False
        
        for line in lines:
            if line.startswith('msgstr') and not line.startswith('msgstr ""'):
                if not last_was_msgstr:
                    result.append(line)
                    last_was_msgstr = True
            else:
                result.append(line)
                last_was_msgstr = False
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result))
        print(f'Fixed {filepath}')
