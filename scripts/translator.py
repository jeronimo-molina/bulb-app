from deep_translator import GoogleTranslator
from polib import pofile
import os
import logging



# Configuração de logs
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

GLOSSARY = {
    'pt': {
        'Wet Bulb': 'Bulbo Úmido',
        'Dew Point': 'Ponto de Orvalho'
    },
    'es': {
        'Wet Bulb': 'Bulbo Húmedo',
        'Dew Point': 'Punto de Rocío'
    }
}

# Função para traduzir arquivos .po
def safe_translate_po(lang):
    po_path = f'translations/{lang}/LC_MESSAGES/messages.po'

    if not os.path.exists(po_path):
        logging.warning(f"Arquivo não encontrado: {po_path}")
        return

    po = pofile(po_path)
    logging.info(f"Traduzindo arquivo: {po_path}")
    
    for entry in po:
        if entry.translated() or entry.fuzzy:
            continue

        # Aplica glossário
        if entry.msgid in GLOSSARY.get(lang, {}):
            entry.msgstr = GLOSSARY[lang][entry.msgid]
            logging.info(f"Glossário aplicado: {entry.msgid} -> {entry.msgstr}")
            continue

        try:
            # Tradução com DeepTranslator
            translated = GoogleTranslator(source="en", target=lang).translate(entry.msgid)
            
            # Validação de placeholders
            if entry.msgid.count('%') != translated.count('%'):
                raise ValueError("Placeholders inconsistentes")
            
            entry.msgstr = translated
            logging.info(f"Traduzido: {entry.msgid} -> {entry.msgstr}")
        except Exception as e:
            logging.error(f"Erro ({lang}): {entry.msgid} - {e}")
            entry.flags.append('fuzzy')  # Marca para revisão

    po.save()
    logging.info(f"Tradução salva em: {po_path}")

# Testes automatizados
def test_translations():
    for lang in ['pt', 'es']:
        po = pofile(f'translations/{lang}/LC_MESSAGES/messages.po')
        for entry in po:
            assert not entry.fuzzy, f"Tradução fuzzy em {lang}: {entry.msgid}"
            if '%(' in entry.msgid:
                assert '%(' in entry.msgstr, f"Placeholder faltante em {lang}: {entry.msgid}"

if __name__ == "__main__":
    for lang in ['pt', 'es']:
        safe_translate_po(lang)
