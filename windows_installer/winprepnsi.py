# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
app_name = "BitTorrent"
from BitTorrent import version
from BTL.language import languages, language_names, locale_sucks
from BitTorrent.NewVersion import Version

NSIS_DIR = "C:\\Program Files\\NSIS"

if not os.path.exists(NSIS_DIR):
    raise Exception("Please set NSIS_DIR in winprepnsi.py!")

currentversion = Version.from_str(version)
version_str = version
if currentversion.is_beta():
    version_str = version_str + '-Beta'

nsis_language_names = {
    'af'    :'Afrikaans',
    'bg'    :'Bulgarian',
    'ca'    :'Catalan',
    'cs'    :'Czech',
    'da'    :'Danish',
    'de'    :'German',
    'en'    :'English',
    'es'    :'Spanish',
    'es_MX' :'SpanishMX',
    'fr'    :'French',
    'el'    :'Greek',
    'hu'    :'Hungarian',
    'he'    :'Hebrew',
    'it'    :'Italian',
    'is'    :'Icelandic',
    'ja'    :'Japanese',
    'ko'    :'Korean',
    'nb_NO' :'Norwegian',
    'nl'    :'Dutch',
    'pl'    :'Polish',
    'pt'    :'Portuguese',
    'pt_BR' :'PortugueseBR',
    'ro'    :'Romanian',
    'ru'    :'Russian',
    'sk'    :'Slovak',
    'sl'    :'Slovenian',
    'sv'    :'Swedish',
    'tr'    :'Turkish',
    'vi'    :'Vietnamese',
    'zh_CN' :'TradChinese',
    'zh_TW' :'SimpChinese',    
    }

    

f = open(sys.argv[1])
b = f.read()
f.close()
b = b.replace("%VERSION%", version_str)
b = b.replace("%APP_NAME%", app_name)

found_langs = {}
lang_macros = ""
for l in languages:
    lang = nsis_language_names[l]
    nlf = os.path.join(NSIS_DIR, "Contrib\\Language files\\%s.nlf" % lang)
    nsh = os.path.join(NSIS_DIR, "Contrib\\Modern UI\\Language files\\%s.nsh" % lang)
    if os.path.exists(nlf) and os.path.exists(nsh):
        lang_macros += ('  !insertmacro MUI_LANGUAGE "%s"\r\n' % lang)
        found_langs[l] = lang
    else:
        lcid = None
        for id, code in locale_sucks.iteritems():
            if code.lower() == l.lower():
                lcid = id
            
        print "Creating a template for", lang, lcid
        f = open(nlf, 'w')
        template = open("windows_installer\\template.nlf", 'r')
        template_str = template.read()
        template.close()
        t = (template_str % {'id':lcid})
        f.write(t)
        f.close()

        f = open(nsh, 'w')
        template = open("windows_installer\\template.nsh", 'r')
        template_str = template.read()
        template.close()
        t = (template_str % {'name':lang, 'id':lcid})
        f.write(t)
        f.close()
             

        lang_macros += ('  !insertmacro MUI_LANGUAGE "%s"\r\n' % lang)
        found_langs[l] = lang

b = b.replace("%LANG_MACROS%", lang_macros)

f = open(sys.argv[2], "w")
f.write(b)
f.close()

