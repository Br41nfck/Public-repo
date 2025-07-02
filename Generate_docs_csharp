#############################################################################################################
# Наименование: Generate_Docs_Csharp.py                                                                     #
# Описание: Генерация документации по <summary> блокам в коде проекта C#                                    #
# ВАЖНО: Для корректной генерации summary-комментарии должны стоять НЕПОСРЕДСТВЕННО перед классом/методом!  #
#                                                                                                           #
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
PARAM_RE = re.compile(r'///\s*<param name="([^"]+)">(.*?)</param>', re.DOTALL)
RETURNS_RE = re.compile(r'///\s*<returns>(.*?)</returns>', re.DOTALL)
ATTR_RE = re.compile(r'^\s*\[(\w+[^\]]*)\]', re.MULTILINE)
INHERIT_RE = re.compile(r'class\s+\w+\s*:\s*([\w\s,<>]+)')


def clean_summary_text(text):
    lines = text.strip().splitlines()
    cleaned = [l.strip().lstrip('/').strip() if l.strip().startswith('///') else l.strip() for l in lines]
    joined = ' '.join(cleaned).strip(' /')
    joined = re.sub(r'<\/?summary>', '', joined, flags=re.IGNORECASE).strip()
    return html.escape(joined)


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

def extract_code_summaries(file_content, filename):
    lines = file_content.splitlines()
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('///') and '<summary>' in line:
            summary_lines = []
            param_docs = {}
            returns_doc = ''
            while i < len(lines) and '///' in lines[i]:
                summary_lines.append(lines[i])
                param_match = re.search(r'<param name="([^"]+)">(.*?)</param>', lines[i])
                if param_match:
                    param_docs[param_match.group(1)] = clean_summary_text(param_match.group(2))
                returns_match = re.search(r'<returns>(.*?)</returns>', lines[i])
                if returns_match:
                    returns_doc = clean_summary_text(returns_match.group(1))
                if '</summary>' in lines[i]:
                    break
                i += 1
            j = i + 1
            while j < len(lines) and (lines[j].strip() == '' or lines[j].strip().startswith('///')):
                j += 1
            if j < len(lines):
                code_line = lines[j].strip()
                attrs = []
                k = j-1
                while k >= 0 and lines[k].strip().startswith('['):
                    attr_line = lines[k].strip()
                    attr_match = ATTR_RE.match(attr_line)
                    if attr_match:
                        attrs.insert(0, attr_match.group(1))
                    k -= 1
                attr_str = ', '.join(attrs)
                mod_match = re.match(r'((public|private|internal|protected|static|partial|virtual|override|sealed|abstract|async)\s+)+', code_line)
                modifiers = mod_match.group(0).strip() if mod_match else ''
                obj_type = None
                obj_name = None
                params = ''
                returns = ''
                inherit = ''
                if re.match(r'(public|private|internal|protected)?\s*(static\s+)?(partial\s+)?class\s+(\w+)', code_line):
                    obj_type = 'Class'
                    obj_name = re.findall(r'class\s+(\w+)', code_line)[0]
                    # Наследование/интерфейсы
                    inh = INHERIT_RE.search(code_line)
                    if inh:
                        inherit = inh.group(1)
                elif re.match(r'(public|private|internal|protected)?\s*(static\s+)?(partial\s+)?(void|[\w<>\[\]]+)\s+(\w+)\s*\(', code_line):
                    obj_type = 'Method'
                    obj_name = re.findall(r'(?:void|[\w<>\[\]]+)\s+(\w+)\s*\(', code_line)[0]
                    # Параметры
                    paren = code_line.find('(')
                    if paren != -1:
                        params = code_line[paren+1:code_line.find(')', paren)]
                    # Возвращаемое значение
                    ret_match = re.match(r'(public|private|internal|protected)?\s*(static\s+)?(partial\s+)?([\w<>\[\]]+)\s+\w+\s*\(', code_line)
                    if ret_match:
                        returns = ret_match.group(4)
                elif re.match(r'(public|private|internal|protected)?\s*(static\s+)?(partial\s+)?[\w<>\[\]]+\s+(\w+)\s*{', code_line):
                    obj_type = 'Property'
                    obj_name = re.findall(r'[\w<>\[\]]+\s+(\w+)\s*{', code_line)[0]
                    ret_match = re.match(r'(public|private|internal|protected)?\s*(static\s+)?(partial\s+)?([\w<>\[\]]+)\s+\w+\s*{', code_line)
                    if ret_match:
                        returns = ret_match.group(4)
                else:
                    obj_type = 'Other'
                    obj_name = code_line[:40]
                summary_text = clean_summary_text('\n'.join(summary_lines))
                signature = lines[j].strip()
                # Строка файла
                line_num = j+1
                results.append({
                    'type': obj_type,
                    'name': obj_name,
                    'summary': summary_text,
                    'signature': signature,
                    'modifiers': modifiers,
                    'attributes': attr_str,
                    'inherit': inherit,
                    'params': params,
                    'param_docs': param_docs,
                    'returns': returns,
                    'returns_doc': returns_doc,
                    'file': filename,
                    'line': line_num
                })
            i = j
        else:
            i += 1
    return results

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
        f.write('<!DOCTYPE html>\n<html lang="ru">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="icon" href="data:,">\n<link rel="stylesheet" href="style.css">\n')
        f.write(f'<h1>Summary по файлу {base}</h1>\n')
        # sticky-оглавление как выпадающий список
        if summaries:
            f.write('<div id="toc" style="position:sticky;top:0;background:#fff;z-index:10;padding:6px 0 6px 0;">')
            f.write('<label for="tocSelect"><b>Оглавление:</b></label> ')
            f.write('<select id="tocSelect" style="min-width:220px;max-width:90vw;">')
            f.write('<option value="all">Показать все</option>')
            for s in summaries:
                anchor = f'{s["type"]}_{s["name"]}_{s["line"]}'
                display = html.escape(s["signature"])
                f.write(f'<option value="{anchor}">{display}</option>')
            f.write('</select> ')
            f.write('<button id="showAllBtn" onclick="showAllRows()" style="display:none;">Показать все</button>')
            f.write('</div>')
        # Кнопки и поиск
        f.write(
        '''<div style="margin:10px 0;"><input type="text" id="searchInput" placeholder="Поиск по таблице..." style="width:300px;"> 
        <button onclick="exportMarkdown()">Экспорт в Markdown</button> 
        <button onclick="exportPDF()">Экспорт в PDF</button> 
        <button onclick="exportCSV()">Экспорт в CSV</button> 
        <button onclick="exportExcel()">Экспорт в Excel</button> 
        <button onclick="exportHTML()">Экспорт в HTML</button> 
        <button onclick="exportDOCX()">Экспорт в DOCX</button> 
        <button onclick="exportJSON()">Экспорт в JSON</button></div>'''
                )

        f.write('<style>\n')
        f.write('table { width: 100%; border-collapse: collapse; }\n')
        f.write('th, td { text-align: justify; vertical-align: top; word-break: break-word; padding: 4px; }\n')
        f.write('tr.hide { display: none; }\n')
        f.write('</style>\n')
        if summaries:
            f.write('<table id="docTable" border="1" cellpadding="4"><tr>'
                    '<th>Тип</th><th>Имя/Сигнатура</th><th>Модификаторы</th><th>Атрибуты</th>'
                    '<th>Наследование/Интерфейсы</th><th>Параметры</th><th>Возвращает</th>'
                    '<th>Файл/Строка</th><th>Summary</th></tr>')
            for s in summaries:
                type_ru = s["type"]
                if type_ru == "Class":
                    type_ru = "Класс"
                elif type_ru == "Method":
                    type_ru = "Метод"
                elif type_ru == "Other":
                    type_ru = "Другое"
                anchor = f'{s["type"]}_{s["name"]}_{s["line"]}'
                signature_html = html.escape(s["signature"])
                param_str = ''
                if s["params"]:
                    param_list = [p.strip() for p in s["params"].split(',') if p.strip()]
                    param_str = '<br>'.join([
                        f'{html.escape(p)}' + (f' <span style="color:gray">({html.escape(s["param_docs"].get(p.split()[-1], ""))})</span>' if s["param_docs"].get(p.split()[-1], "") else '')
                        for p in param_list])
                returns_str = html.escape(s["returns"])
                if s["returns_doc"]:
                    returns_str += f'<br><span style="color:gray">{html.escape(s["returns_doc"])}"</span>'
                f.write(f'<tr id="{anchor}"><td>{type_ru}</td>'
                        f'<td title="{signature_html}">{signature_html}</td>'
                        f'<td>{html.escape(s["modifiers"])}</td>'
                        f'<td>{html.escape(s["attributes"])}</td>'
                        f'<td>{html.escape(s["inherit"])}</td>'
                        f'<td>{param_str}</td>'
                        f'<td>{returns_str}</td>'
                        f'<td>{html.escape(s["file"])}:{s["line"]}</td>'
                        f'<td>{s["summary"]}</td></tr>')
            f.write('</table>\n')
        else:
            f.write('<p><i>Нет summary-комментариев в этом файле.</i></p>')
        f.write('<a href="index.html">На главную</a>')
        f.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>\n')
        f.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js"></script>\n')
        f.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>\n')
        f.write('<script src="https://cdn.jsdelivr.net/npm/docx@8.3.0/build/index.umd.min.js"></script>\n')
        f.write('<script src="export.js"></script>\n')
    return html_name

# Создание INDEX-файла
def write_index_html(docs_dir, file_links):
    dt = datetime.datetime.now()
    months = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    last_modified = f'{dt.day} {months[dt.month]} {dt.year} г. {dt:%H:%M:%S}'
    with open(os.path.join(docs_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html lang="ru">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="icon" href="data:,">\n<link rel="stylesheet" href="style.css">\n')
        f.write('<h1>Документация по Автотесту</h1>\n')
        f.write(f'<p><em>Последнее изменение файла: {last_modified}</em></p>\n')
        
        # Поиск по файлам
        f.write('<input type="text" id="searchInput" placeholder="Поиск по файлам..." style="width:300px;margin-bottom:10px;">\n')
        f.write('<ul id="fileList">')
        for base, html_name in file_links:
            f.write(f'<li><a href="{html_name}">{base}</a></li>\n')
        f.write('</ul>')
       
       # JS для поиска
        f.write('''<script>
const searchInput = document.getElementById('searchInput');
const fileList = document.getElementById('fileList');
searchInput.addEventListener('input', function() {
  const val = this.value.toLowerCase();
  for (const li of fileList.children) {
    li.style.display = li.textContent.toLowerCase().includes(val) ? '' : 'none';
  }
});
</script>''')

# Основная функция 
def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    cs_files = scan_cs_files(SRC_DIR)
    file_links = []
    for cs_file in cs_files:
        with open(cs_file, encoding='utf-8') as f:
            content = f.read()
        summaries = extract_code_summaries(content, os.path.basename(cs_file))
        if summaries:
            html_name = write_file_summaries_html(DOCS_DIR, cs_file, summaries)
            file_links.append((os.path.basename(cs_file), html_name))
    file_links.sort(key=lambda x: x[0].lower())
    write_index_html(DOCS_DIR, file_links)
    print(f'Документация по Автотесту сгенерирована в папку {DOCS_DIR}')

if __name__ == '__main__':
    main()
