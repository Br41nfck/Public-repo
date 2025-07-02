#############################################################################################################
# Наименование: Generate_Docs_Csharp.py                                                                     #
# Описание: Генерация документации по <summary> блокам в коде проекта C#                                    #
# Дата: 02.07.2025                                                                                          #
# How-to-Use:                                                                                               #
# 1) Скопировать файл в папку с .cs-файлами                                                                 #
# 2) 3апустить команду (в консоли или cmd) python Generate_Docs.py                                          #
# HTML-файлы будут находиться в /docs в директории проекта (DOCS_DIR можно заменить на собственную)         #
# index.html - основной файл для перемещения по файлам документации                                         #
#############################################################################################################

import os
import re
import html
import datetime

SRC_DIR = '.'       # Папка с .cs-файлами
DOCS_DIR = 'docs'   # Куда складывать HTML

SUMMARY_RE = re.compile(r'///\s*<summary>(.*?)</summary>', re.DOTALL)
CLASS_RE = re.compile(r'(///\s*<summary>(.*?)</summary>\s*)?(public|internal|private|protected)?\s*(partial\s+)?class\s+(\w+)', re.DOTALL)

# Удаление "///"
def clean_summary_text(text):
    lines = text.strip().splitlines()
    cleaned = [l.strip().lstrip('/').strip() if l.strip().startswith('///') else l.strip() for l in lines]
    return html.escape(' '.join(cleaned).strip(' /'))

# Извлечение summary по классу 
def extract_class_summaries(file_content):
    result = []
    for m in CLASS_RE.finditer(file_content):
        class_name = m.group(5)
        class_summary = m.group(2)
        if class_summary:
            class_summary = clean_summary_text(class_summary)
        else:
            class_summary = ''
        result.append({'name': class_name, 'summary': class_summary, 'pos': m.start()})
    return result

# Извлечение всех summary
def extract_all_summaries(file_content):
    summaries = []
    class_summaries = extract_class_summaries(file_content)
    for m in SUMMARY_RE.finditer(file_content):
        before = file_content[:m.start()]
        lines = before.splitlines()
        context = ''
        for line in reversed(lines[-15:]):
            lstr = line.strip()
            if lstr.startswith('///') or not lstr:
                continue
            if 'class ' in lstr or 'struct ' in lstr or 'interface ' in lstr:
                context = lstr
                break
            if '(' in lstr and ')' in lstr:
                context = lstr
                break
            if '{ get;' in lstr:
                context = lstr
                break
            if not context:
                context = lstr
        if context.startswith('///'):
            context = context.lstrip('/').strip()
        summary_text = clean_summary_text(m.group(1))
        if context.strip() == '{':
            class_desc = ''
            for c in reversed(class_summaries):
                if c['pos'] < m.start():
                    class_desc = c['summary']
                    break
            if class_desc:
                context = class_desc
            else:
                context = '<b>Описание класса</b>'
        summaries.append({'context': context if context else '[нет контекста выше]', 'summary': summary_text})
    return summaries

# Сканирование файлов в папке со скриптом 
# AssemblyInfo, AssemblyAttributes, GlobalUsings, Designer убраны из генерации документации
def scan_cs_files(src_dir):
    cs_files = [os.path.join(root, f)
                for root, _, files in os.walk(src_dir)
                for f in files if f.endswith('.cs')
                and 'AssemblyInfo' not in f and 'AssemblyAttributes' not in f and 'GlobalUsings' not in f and 'Designer' not in f]
    return cs_files

# Запись всех summary из .cs-файла в HTML-файл
def write_file_summaries_html(docs_dir, cs_file, summaries):
    base = os.path.basename(cs_file)
    html_name = f'{base}.html'
    with open(os.path.join(docs_dir, html_name), 'w', encoding='utf-8') as f:
        f.write(f'<h1>Summary по файлу {base}</h1>\n')
        if summaries:
            f.write('<table border="1" cellpadding="4"><tr><th>Контекст</th><th>Summary</th></tr>')
            for s in summaries:
                f.write(f'<tr><td>{s["context"]}</td><td>{s["summary"]}</td></tr>')
            f.write('</table>\n')
        else:
            f.write('<p><i>Нет summary-комментариев в этом файле.</i></p>')
        f.write('<a href="index.html">На главную</a>')
    return html_name

# Создание INDEX-файла
def write_index_html(docs_dir, file_links):
    # Получаем текущее время
    dt = datetime.datetime.now()
    months = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    last_modified = f'{dt.day} {months[dt.month]} {dt.year} г. {dt:%H:%M:%S}'
    with open(os.path.join(docs_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write('<h1>Документация по Автотесту</h1>\n')
        f.write(f'<p><em>Последнее изменение файла: {last_modified}</em></p>\n')
        f.write('<ul>')
        for base, html_name in file_links:
            f.write(f'<li><a href="{html_name}">{base}</a></li>\n')
        f.write('</ul>')

# Основная функция 
def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    cs_files = scan_cs_files(SRC_DIR)
    file_links = []
    for cs_file in cs_files:
        with open(cs_file, encoding='utf-8') as f:
            content = f.read()
        summaries = extract_all_summaries(content)
        html_name = write_file_summaries_html(DOCS_DIR, cs_file, summaries)
        file_links.append((os.path.basename(cs_file), html_name))
    file_links.sort(key=lambda x: x[0].lower())  # сортировка по имени файла
    write_index_html(DOCS_DIR, file_links)
    print(f'Документация по Автотесту сгенерирована в папку {DOCS_DIR}')

if __name__ == '__main__':
    main()