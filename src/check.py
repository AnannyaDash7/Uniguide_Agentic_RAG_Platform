import os
import glob
import csv

pdfs = {
    os.path.basename(p).strip()[:-4]
    for p in glob.glob('data/raw/*.pdf')
}

meta = {
    r['doc_id'].strip().removesuffix('.pdf')
    for r in csv.DictReader(
        open('data/metadata.csv', encoding='utf-8')
    )
}

print('PDFs without metadata:', pdfs - meta)
print('Metadata without PDF:', meta - pdfs)