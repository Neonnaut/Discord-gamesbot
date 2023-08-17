from discord import Embed
import discord
import random

from constants import ERR, CHECK

# Here we get all flags
already_countries = []

countries = [
    {
        'names': ['Jordan','Hashemite Kingdom of Jordan','الأردن','المملكة الأردنية الهاشمية'],
        'flag': 'https://flagcdn.com/w320/jo.png'
    },
    {
        'names': ['Serbia','Republic of Serbia','Република Србија','Србија'],
        'flag': 'https://flagcdn.com/w320/rs.png'
    },
    {
        'names': ['Andorra','Principality of Andorra',"Principat d'Andorra"],
        'flag': 'https://flagcdn.com/w320/ad.png'
    },
    {
        'names': ['Bolivia','Buliwya','Buliwya Mamallaqta','Estado Plurinacional de Bolivia','Plurinational State of Bolivia','Tetã Volívia','Volívia','Wuliwya','Wuliwya Suyu'],
        'flag': 'https://flagcdn.com/w320/bo.png'
    },
    {
        'names': ['Libya','State of Libya','الدولة ليبيا','\u200fليبيا'],
        'flag': 'https://flagcdn.com/w320/ly.png'
    },
    {
        'names': ['Mali','Republic of Mali','République du Mali'],
        'flag': 'https://flagcdn.com/w320/ml.png'
    },
    {
        'names': ['Armenia','Republic of Armenia','Հայաստան','Հայաստանի Հանրապետություն'],
        'flag': 'https://flagcdn.com/w320/am.png'
    },
    {
        'names': ['Mauritius','Maurice','Moris','Republic of Mauritius','Republik Moris','République de Maurice'],
        'flag': 'https://flagcdn.com/w320/mu.png'
    },
    {
        'names': ['Maldives','Republic of the Maldives','ދިވެހިރާއްޖޭގެ','ދިވެހިރާއްޖޭގެ ޖުމްހޫރިއްޔާ'],
        'flag': 'https://flagcdn.com/w320/mv.png'
    },
    {
        'names': ['North Macedonia','Republic of North Macedonia','Македонија','Република Северна Македонија'],
        'flag': 'https://flagcdn.com/w320/mk.png'
    },
    {
        'names': ['Ethiopia','Federal Democratic Republic of Ethiopia','ኢትዮጵያ','የኢትዮጵያ ፌዴራላዊ ዲሞክራሲያዊ ሪፐብሊክ'],
        'flag': 'https://flagcdn.com/w320/et.png'
    },
    {
        'names': ['Iraq','Republic of Iraq','العراق','جمهورية العراق','کۆماری','کۆماری عێراق','ܩܘܼܛܢܵܐ','ܩܘܼܛܢܵܐ ܐܝܼܪܲܩ'],
        'flag': 'https://flagcdn.com/w320/iq.png'
    },
    {
        'names': ['Guatemala','Republic of Guatemala','República de Guatemala'],
        'flag': 'https://flagcdn.com/w320/gt.png'
    },
    {
        'names': ['Trinidad and Tobago','Republic of Trinidad and Tobago'],
        'flag': 'https://flagcdn.com/w320/tt.png'
    },
    {
        'names': ['Peru','Perú','Piruw','Piruw Ripuwlika','Piruw Suyu','Republic of Peru','República del Perú'],
        'flag': 'https://flagcdn.com/w320/pe.png'
    },
    {
        'names': ['Suriname','Republic of Suriname','Republiek Suriname'],
        'flag': 'https://flagcdn.com/w320/sr.png'
    },
    {
        'names': ['Sweden','Kingdom of Sweden','Konungariket Sverige','Sverige'],
        'flag': 'https://flagcdn.com/w320/se.png'
    },
    {
        'names': ['Benin','Bénin','Republic of Benin','République du Bénin'],
        'flag': 'https://flagcdn.com/w320/bj.png'
    },
    {
        'names': ['Estonia','Eesti','Eesti Vabariik','Republic of Estonia'],
        'flag': 'https://flagcdn.com/w320/ee.png'
    },
    {
        'names': ['Zimbabwe','Republic of Zimbabwe'],
        'flag': 'https://flagcdn.com/w320/zw.png'
    },
    {
        'names': ['Slovakia','Slovak Republic','Slovensko','Slovenská republika'],
        'flag': 'https://flagcdn.com/w320/sk.png'
    },
    {
        'names': ['Netherlands','The Netherlands','Kingdom of the Netherlands','Koninkrijk der Nederlanden','Nederland'],
        'flag': 'https://flagcdn.com/w320/nl.png'
    },
    {
        'names': ['Ecuador','Republic of Ecuador','República del Ecuador'],
        'flag': 'https://flagcdn.com/w320/ec.png'
    },
    {
        'names': ['Saudi Arabia','Kingdom of Saudi Arabia','العربية السعودية','المملكة العربية السعودية'],
        'flag': 'https://flagcdn.com/w320/sa.png'
    },
    {
        'names': ['United Arab Emirates','الإمارات العربية المتحدة','دولة الإمارات العربية المتحدة'],
        'flag': 'https://flagcdn.com/w320/ae.png'
    },
    {
        'names': ['Afghanistan','Islamic Republic of Afghanistan','Owganystan','Owganystan Yslam Respublikasy','افغانستان','جمهوری اسلامی افغانستان','د افغانستان اسلامي جمهوریت'],
        'flag': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_the_Taliban.svg/320px-Flag_of_the_Taliban.svg.png'
    },
    {
        'names': ['Central African Republic','Bêafrîka','Ködörösêse tî Bêafrîka','République centrafricaine'],
        'flag': 'https://flagcdn.com/w320/cf.png'
    },
    {
        'names': ['Panama','Panamá','Republic of Panama','República de Panamá'],
        'flag': 'https://flagcdn.com/w320/pa.png'
    },
    {
        'names': ['Vatican City','Stato della Città del Vaticano','Status Civitatis Vaticanæ','Vatican City State','Vaticano','Vaticanæ'],
        'flag': 'https://flagcdn.com/w320/va.png'
    },
    {
        'names': ['Syria','Syrian Arab Republic','الجمهورية العربية السورية','سوريا'],
        'flag': 'https://flagcdn.com/w320/sy.png'
    },
    {
        'names': ['Vanuatu','Republic of Vanuatu','Ripablik blong Vanuatu','République de Vanuatu'],
        'flag': 'https://flagcdn.com/w320/vu.png'
    },
    {
        'names': ['Honduras','Republic of Honduras','República de Honduras'],
        'flag': 'https://flagcdn.com/w320/hn.png'
    },
    {
        'names': ['Kiribati','Independent and Sovereign Republic of Kiribati','Ribaberiki Kiribati'],
        'flag': 'https://flagcdn.com/w320/ki.png'
    },
    {
        'names': ['Chile','Republic of Chile','República de Chile'],
        'flag': 'https://flagcdn.com/w320/cl.png'
    },
    {
        'names': ['Burkina Faso','République du Burkina'],
        'flag': 'https://flagcdn.com/w320/bf.png'
    },
    {
        'names': ['Saint Kitts and Nevis','Federation of Saint Christopher and Nevis'],
        'flag': 'https://flagcdn.com/w320/kn.png'
    },
    {
        'names': ['Mexico','Estados Unidos Mexicanos','México','United Mexican States'],
        'flag': 'https://flagcdn.com/w320/mx.png'
    },
    {
        'names': ['China',"People's Republic of China",'中华人民共和国','中国'],
        'flag': 'https://flagcdn.com/w320/cn.png'
    },
    {
        'names': ['East Timor','Timor-Leste','Democratic Republic of Timor-Leste','República Democrática de Timor-Leste','Repúblika Demokrátika Timór-Leste','Timór-Leste'],
        'flag': 'https://flagcdn.com/w320/tl.png'
    },
    {
        'names': ['South Sudan','Republic of South Sudan'],
        'flag': 'https://flagcdn.com/w320/ss.png'
    },
    {
        'names': ['Eswatini','Kingdom of Eswatini','Umbuso weSwatini','eSwatini'],
        'flag': 'https://flagcdn.com/w320/sz.png'
    },
    {
        'names': ['Uzbekistan',"O'zbekiston Respublikasi",'O‘zbekiston','Republic of Uzbekistan','Uzbekistan','Республика Узбекистан','Узбекистан'],
        'flag': 'https://flagcdn.com/w320/uz.png'
    },
    {
        'names': ['Indonesia','Republic of Indonesia','Republik Indonesia'],
        'flag': 'https://flagcdn.com/w320/id.png'
    },
    {
        'names': ['Paraguay','Paraguái','Republic of Paraguay','República de Paraguay','Tetã Paraguái'],
        'flag': 'https://flagcdn.com/w320/py.png'
    },
    {
        'names': ['Monaco','Principality of Monaco','Principauté de Monaco'],
        'flag': 'https://flagcdn.com/w320/mc.png'
    },
    {
        'names': ['Grenada'],
        'flag': 'https://flagcdn.com/w320/gd.png'
    },
    {
        'names': ['Croatia','Hrvatska','Republic of Croatia','Republika Hrvatska'],
        'flag': 'https://flagcdn.com/w320/hr.png'
    },
    {
        'names': ['Poland','Polska','Republic of Poland','Rzeczpospolita Polska'],
        'flag': 'https://flagcdn.com/w320/pl.png'
    },
    {
        'names': ['Bosnia and Herzegovina','Bosna i Hercegovina','Босна и Херцеговина'],
        'flag': 'https://flagcdn.com/w320/ba.png'
    },
    {
        'names': ['Canada'],
        'flag': 'https://flagcdn.com/w320/ca.png'
    },
    {
        'names': ['Portugal','Portuguese Republic','República português'],
        'flag': 'https://flagcdn.com/w320/pt.png'
    },
    {
        'names': ['Brazil','Brasil','Federative Republic of Brazil','República Federativa do Brasil'],
        'flag': 'https://flagcdn.com/w320/br.png'
    },
    {
        'names': ['Mauritania','Islamic Republic of Mauritania','الجمهورية الإسلامية الموريتانية','موريتانيا'],
        'flag': 'https://flagcdn.com/w320/mr.png'
    },
    {
        'names': ['Israel','State of Israel','ישראל','מדינת ישראל','إسرائيل','دولة إسرائيل'],
        'flag': 'https://flagcdn.com/w320/il.png'
    },
    {
        'names': ['Brunei','Nation of Brunei, Abode Damai','Nation of Brunei, Abode of Peace','Negara Brunei Darussalam'],
        'flag': 'https://flagcdn.com/w320/bn.png'
    },
    {
        'names': ['Angola','Republic of Angola','República de Angola'],
        'flag': 'https://flagcdn.com/w320/ao.png'
    },
    {
        'names': ['Malta',"Repubblika ta ' Malta",'Republic of Malta'],
        'flag': 'https://flagcdn.com/w320/mt.png'
    },
    {
        'names': ['Belarus','Republic of Belarus','Белару́сь','Беларусь','Республика Беларусь','Рэспубліка Беларусь'],
        'flag': 'https://flagcdn.com/w320/by.png'
    },
    {
        'names': ['Turkey','Republic of Turkey','Türkiye','Türkiye Cumhuriyeti'],
        'flag': 'https://flagcdn.com/w320/tr.png'
    },
    {
        'names': ['Finland','Republic of Finland','Republiken Finland','Suomen tasavalta','Suomi'],
        'flag': 'https://flagcdn.com/w320/fi.png'
    },
    {
        'names': ['Bhutan','Kingdom of Bhutan','འབྲུག་ཡུལ་','འབྲུག་རྒྱལ་ཁབ་'],
        'flag': 'https://flagcdn.com/w320/bt.png'
    },
    {
        'names': ['Spain','España','Kingdom of Spain','Reino de España'],
        'flag': 'https://flagcdn.com/w320/es.png'
    },
    {
        'names': ['Venezuela','Bolivarian Republic of Venezuela','República Bolivariana de Venezuela'],
        'flag': 'https://flagcdn.com/w320/ve.png'
    },
    {
        'names': ['Qatar','State of Qatar','دولة قطر','قطر'],
        'flag': 'https://flagcdn.com/w320/qa.png'
    },
    {
        'names': ['Czechia','Czech Republic','Česko','Česká republika'],
        'flag': 'https://flagcdn.com/w320/cz.png'
    },
    {
        'names': ['Kuwait','State of Kuwait','الكويت','دولة الكويت'],
        'flag': 'https://flagcdn.com/w320/kw.png'
    },
    {
        'names': ['Montenegro','Црна Гора'],
        'flag': 'https://flagcdn.com/w320/me.png'
    },
    {
        'names': ['India','Republic of India','भारत','भारत गणराज्य','இந்தியக் குடியரசு','இந்தியா'],
        'flag': 'https://flagcdn.com/w320/in.png'
    },
    {
        'names': ['New Zealand','Aotearoa'],
        'flag': 'https://flagcdn.com/w320/nz.png'
    },
    {
        'names': ['Jamaica'],
        'flag': 'https://flagcdn.com/w320/jm.png'
    },
    {
        'names': ['San Marino','Repubblica di San Marino','Republic of San Marino'],
        'flag': 'https://flagcdn.com/w320/sm.png'
    },
    {
        'names': ['Republic of the Congo','Repubilika ya Kongo','Republíki ya Kongó','République du Congo'],
        'flag': 'https://flagcdn.com/w320/cg.png'
    },
    {
        'names': ['Pakistan','Islamic Republic of Pakistan','اسلامی جمہوریۂ پاكستان','پاكستان'],
        'flag': 'https://flagcdn.com/w320/pk.png'
    },
    {
        'names': ['France','French Republic','République française'],
        'flag': 'https://flagcdn.com/w320/fr.png'
    },
    {
        'names': ['Kazakhstan','Republic of Kazakhstan','Казахстан','Республика Казахстан','Қазақстан','Қазақстан Республикасы'],
        'flag': 'https://flagcdn.com/w320/kz.png'
    },
    {
        'names': ['Bahrain','Kingdom of Bahrain','مملكة البحرين','\u200fالبحرين'],
        'flag': 'https://flagcdn.com/w320/bh.png'
    },
    {
        'names': ['Fiji','Matanitu Tugalala o Viti','Republic of Fiji','Viti','फिजी','रिपब्लिक ऑफ फीजी'],
        'flag': 'https://flagcdn.com/w320/fj.png'
    },
    {
        'names': ['Iceland','Ísland'],
        'flag': 'https://flagcdn.com/w320/is.png'
    },
    {
        'names': ['Myanmar','Burma','Republic of the Union of Myanmar','ပြည်ထောင်စု သမ္မတ မြန်မာနိုင်ငံတော်','မြန်မာ'],
        'flag': 'https://flagcdn.com/w320/mm.png'
    },
    {
        'names': ['Bangladesh',"People's Republic of Bangladesh",'বাংলাদেশ','বাংলাদেশ গণপ্রজাতন্ত্রী'],
        'flag': 'https://flagcdn.com/w320/bd.png'
    },
    {
        'names': ['Philippines','Pilipinas','Republic of the Philippines'],
        'flag': 'https://flagcdn.com/w320/ph.png'
    },
    {
        'names': ['Equatorial Guinea','Guinea Ecuatorial','Guiné Equatorial','Guinée équatoriale','Republic of Equatorial Guinea','República da Guiné Equatorial','República de Guinea Ecuatorial','République de la Guinée Équatoriale'],
        'flag': 'https://flagcdn.com/w320/gq.png'
    },
    {
        'names': ['Ireland','Poblacht na hÉireann','Republic of Ireland','Éire'],
        'flag': 'https://flagcdn.com/w320/ie.png'
    },
    {
        'names': ['Nepal','Federal Democratic Republic of Nepal','नेपाल','नेपाल संघीय लोकतान्त्रिक गणतन्त्र'],
        'flag': 'https://flagcdn.com/w320/np.png'
    },
    {
        'names': ['Yemen','Republic of Yemen','الجمهورية اليمنية','اليَمَن'],
        'flag': 'https://flagcdn.com/w320/ye.png'
    },
    {
        'names': ['South Korea','Korea','Republic of Korea','대한민국','한국'],
        'flag': 'https://flagcdn.com/w320/kr.png'
    },
    {
        'names': ['Denmark','Danmark','Kingdom of Denmark','Kongeriget Danmark'],
        'flag': 'https://flagcdn.com/w320/dk.png'
    },
    {
        'names': ['Oman','Sultanate of Oman','سلطنة عمان','عمان'],
        'flag': 'https://flagcdn.com/w320/om.png'
    },
    {
        'names': ['Saint Vincent and the Grenadines'],
        'flag': 'https://flagcdn.com/w320/vc.png'
    },
    {
        'names': ['Eritrea','State of Eritrea','إرتريا\u200e','دولة إرتريا','ሃገረ ኤርትራ','ኤርትራ'],
        'flag': 'https://flagcdn.com/w320/er.png'
    },
    {
        'names': ['Australia','Commonwealth of Australia'],
        'flag': 'https://flagcdn.com/w320/au.png'
    },
    {
        'names': ['Iran','Islamic Republic of Iran','ایران','جمهوری اسلامی ایران'],
        'flag': 'https://flagcdn.com/w320/ir.png'
    },
    {
        'names': ['El Salvador','Republic of El Salvador','República de El Salvador'],
        'flag': 'https://flagcdn.com/w320/sv.png'
    },
    {
        'names': ['Tanzania','Jamhuri ya Muungano wa Tanzania','United Republic of Tanzania'],
        'flag': 'https://flagcdn.com/w320/tz.png'
    },
    {
        'names': ['Solomon Islands'],
        'flag': 'https://flagcdn.com/w320/sb.png'
    },
    {
        'names': ['Kenya','Republic of Kenya'],
        'flag': 'https://flagcdn.com/w320/ke.png'
    },
    {
        'names': ['Dominican Republic','República Dominicana'],
        'flag': 'https://flagcdn.com/w320/do.png'
    },
    {
        'names': ['Greece','Hellenic Republic','Ελλάδα','Ελληνική Δημοκρατία'],
        'flag': 'https://flagcdn.com/w320/gr.png'
    },
    {
        'names': ['Rwanda','Republic of Rwanda',"Repubulika y'u Rwanda",'République rwandaise'],
        'flag': 'https://flagcdn.com/w320/rw.png'
    },
    {
        'names': ['Tuvalu'],
        'flag': 'https://flagcdn.com/w320/tv.png'
    },
    {
        'names': ['Taiwan','Republic of China','中華民國','台灣'],
        'flag': 'https://flagcdn.com/w320/tw.png'
    },
    {
        'names': ['Guyana','Co-operative Republic of Guyana'],
        'flag': 'https://flagcdn.com/w320/gy.png'
    },
    {
        'names': ['Seychelles','Repiblik Sesel','Republic of Seychelles','République des Seychelles','Sesel'],
        'flag': 'https://flagcdn.com/w320/sc.png'
    },
    {
        'names': ['North Korea','조선','조선민주주의인민공화국'],
        'flag': 'https://flagcdn.com/w320/kp.png'
    },
    {
        'names': ['Botswana','Lefatshe la Botswana','Republic of Botswana'],
        'flag': 'https://flagcdn.com/w320/bw.png'
    },
    {
        'names': ['Cambodia','Kingdom of Cambodia','Kâmpŭchéa','ព្រះរាជាណាចក្រកម្ពុជា'],
        'flag': 'https://flagcdn.com/w320/kh.png'
    },
    {
        'names': ['Barbados'],
        'flag': 'https://flagcdn.com/w320/bb.png'
    },
    {
        'names': ['Colombia','Republic of Colombia','República de Colombia'],
        'flag': 'https://flagcdn.com/w320/co.png'
    },
    {
        'names': ['Ukraine','Україна'],
        'flag': 'https://flagcdn.com/w320/ua.png'
    },
    {
        'names': ['Ivory Coast',"Côte d'Ivoire","Republic of Côte d'Ivoire",
    "République de Côte d'Ivoire"],
        'flag': 'https://flagcdn.com/w320/ci.png'
    },
    {
        'names': ['Nauru','Republic of Nauru'],
        'flag': 'https://flagcdn.com/w320/nr.png'
    },
    {
        'names': ['Namibia','Lefatshe la Namibia','Namibië','Republic of Namibia',
    'Republiek van Namibië','Republik Namibia'],
        'flag': 'https://flagcdn.com/w320/na.png'
    },
    {
        'names': ['Chad','Republic of Chad','République du Tchad','Tchad','تشاد\u200e',
    'جمهورية تشاد'],
        'flag': 'https://flagcdn.com/w320/td.png'
    },
    {
        'names': ['Tonga','Kingdom of Tonga'],
        'flag': 'https://flagcdn.com/w320/to.png'
    },
    {
        'names': ['Argentina','Argentine Republic','República Argentina'],
        'flag': 'https://flagcdn.com/w320/ar.png'
    },
    {
        'names': ['Niger','Republic of Niger','République du Niger'],
        'flag': 'https://flagcdn.com/w320/ne.png'
    },
    {
        'names': ['Marshall Islands','M̧ajeļ','Republic of the Marshall Islands'],
        'flag': 'https://flagcdn.com/w320/mh.png'
    },
    {
        'names': ['Costa Rica','Republic of Costa Rica','República de Costa Rica'],
        'flag': 'https://flagcdn.com/w320/cr.png'
    },
    {
        'names': ['Ghana','Republic of Ghana'],
        'flag': 'https://flagcdn.com/w320/gh.png'
    },
    {
        'names': ['Austria','Republic of Austria','Republik Österreich','Österreich'],
        'flag': 'https://flagcdn.com/w320/at.png'
    },
    {
        'names': ['Palestine','State of Palestine','دولة فلسطين','فلسطين'],
        'flag': 'https://flagcdn.com/w320/ps.png'
    },
    {
        'names': ['Cuba','Republic of Cuba','República de Cuba'],
        'flag': 'https://flagcdn.com/w320/cu.png'
    },
    {
        'names': ['Hungary','Magyarország'],
        'flag': 'https://flagcdn.com/w320/hu.png'
    },
    {
        'names': ['Micronesia','Federated States of Micronesia'],
        'flag': 'https://flagcdn.com/w320/fm.png'
    },
    {
        'names': ['Belize','Belice'],
        'flag': 'https://flagcdn.com/w320/bz.png'
    },
    {
        'names': ['Bahamas','Commonwealth of the Bahamas'],
        'flag': 'https://flagcdn.com/w320/bs.png'
    },
    {
        'names': ['São Tomé and Príncipe','Democratic Republic of São Tomé and Príncipe','República Democrática do São Tomé e Príncipe','São Tomé e Príncipe'],
        'flag': 'https://flagcdn.com/w320/st.png'
    },
    {
        'names': ['Russia','Russian Federation','Российская Федерация','Россия'],
        'flag': 'https://flagcdn.com/w320/ru.png'
    },
    {
        'names': ['Luxembourg','Grand Duchy of Luxembourg','Grand-Duché de Luxembourg','Groussherzogtum Lëtzebuerg','Großherzogtum Luxemburg','Luxemburg','Lëtzebuerg'],
        'flag': 'https://flagcdn.com/w320/lu.png'
    },
    {
        'names': ['Nicaragua','Republic of Nicaragua','República de Nicaragua'],
        'flag': 'https://flagcdn.com/w320/ni.png'
    },
    {
        'names': ['Tunisia','Tunisian Republic','الجمهورية التونسية','تونس'],
        'flag': 'https://flagcdn.com/w320/tn.png'
    },
    {
        'names': ['DR Congo','Democratic Republic of the Congo','Ditunga dia Kongu wa Mungalaata','Jamhuri ya Kidemokrasia ya Kongo',],
        'flag': 'https://flagcdn.com/w320/cd.png'
    },
    {
        'names': ['South Africa','Republic of South Africa','Suid-Afrika','Republiek van Suid-Afrika','Iningizimu Afrika'],
        'flag': 'https://flagcdn.com/w320/za.png'
    },
    {
        'names': ['Sierra Leone','Republic of Sierra Leone'],
        'flag': 'https://flagcdn.com/w320/sl.png'
    },
    {
        'names': ['Lesotho','Kingdom of Lesotho'],
        'flag': 'https://flagcdn.com/w320/ls.png'
    },
    {
        'names': ['Italy','Italia','Italian Republic','Repubblica italiana'],
        'flag': 'https://flagcdn.com/w320/it.png'
    },
    {
        'names': ['Djibouti','Republic of Djibouti','République de Djibouti',
    'جمهورية جيبوتي','جيبوتي\u200e'],
        'flag': 'https://flagcdn.com/w320/dj.png'
    },
    {
        'names': ['Sri Lanka','Democratic Socialist Republic of Sri Lanka','இலங்கை',
        'இலங்கை சனநாயக சோசலிசக் குடியரசு',
        'ශ්\u200dරී ලංකා ප්\u200dරජාතාන්ත්\u200dරික සමාජවාදී ජනරජය',
        'ශ්\u200dරී ලංකාව'],
        'flag': 'https://flagcdn.com/w320/lk.png'
    },
    {
        'names': ['Saint Lucia'],
        'flag': 'https://flagcdn.com/w320/lc.png'
    },
    {
        'names': ['Samoa','Independent State of Samoa','Malo Saʻoloto Tutoʻatasi o Sāmoa',
    'Sāmoa'],
        'flag': 'https://flagcdn.com/w320/ws.png'
    },
    {
        'names': ['Gabon','Gabonese Republic','République gabonaise'],
        'flag': 'https://flagcdn.com/w320/ga.png'
    },
    {
        'names': ['Turkmenistan','Türkmenistan','Туркменистан','Туркмения'],
        'flag': 'https://flagcdn.com/w320/tm.png'
    },
    {
        'names': ['Latvia','Latvija','Latvijas Republikas','Republic of Latvia'],
        'flag': 'https://flagcdn.com/w320/lv.png'
    },
    {
        'names': ['Senegal','Republic of Senegal','République du Sénégal','Sénégal'],
        'flag': 'https://flagcdn.com/w320/sn.png'
    },
    {
        'names': ['Belgium','Belgien','Belgique','België','Kingdom of Belgium',
    'Koninkrijk België','Königreich Belgien','Royaume de Belgique'],
        'flag': 'https://flagcdn.com/w320/be.png'
    },
    {
        'names': ['Moldova','Republic of Moldova','Republica Moldova'],
        'flag': 'https://flagcdn.com/w320/md.png'
    },
    {
        'names': ['Liechtenstein','Fürstentum Liechtenstein','Principality of Liechtenstein'],
        'flag': 'https://flagcdn.com/w320/li.png'
    },
    {
        'names': ['Malawi','Chalo cha Malawi, Dziko la Malaŵi','Malaŵi','Republic of Malawi'],
        'flag': 'https://flagcdn.com/w320/mw.png'
    },
    {
        'names': ['Lebanon','Lebanese Republic','Liban','République libanaise','الجمهورية اللبنانية','لبنان'],
        'flag': 'https://flagcdn.com/w320/lb.png'
    },
    {
        'names': ['Mongolia','Монгол улс'],
        'flag': 'https://flagcdn.com/w320/mn.png'
    },
    {
        'names': ['Norway','Kingdom of Norway','Kongeriket Noreg','Kongeriket Norge','Noreg','Norge','Norgga','Norgga gonagasriika',],
        'flag': 'https://flagcdn.com/w320/no.png'
    },
    {
        'names': ['Cameroon','Cameroun','Republic of Cameroon','République du Cameroun'],
        'flag': 'https://flagcdn.com/w320/cm.png'
    },
    {
        'names': ['Thailand','Kingdom of Thailand','ประเทศไทย','ราชอาณาจักรไทย'],
        'flag': 'https://flagcdn.com/w320/th.png'
    },
    {
        'names': ['Nigeria','Federal Republic of Nigeria'],
        'flag': 'https://flagcdn.com/w320/ng.png'
    },
    {
        'names': ['Cape Verde','Cabo Verde','Republic of Cabo Verde','República de Cabo Verde'],
        'flag': 'https://flagcdn.com/w320/cv.png'
    },
    {
        'names': ['Algeria',"People's Democratic Republic of Algeria",'الجزائر','الجمهورية الديمقراطية الشعبية الجزائرية'],
        'flag': 'https://flagcdn.com/w320/dz.png'
    },
    {
        'names': ['Laos',"Lao People's Democratic Republic",'ສປປລາວ','ສາທາລະນະ ຊາທິປະໄຕ ຄົນລາວ ຂອງ'],
        'flag': 'https://flagcdn.com/w320/la.png'
    },
    {
        'names': ['Azerbaijan','Azərbaycan','Azərbaycan Respublikası','Republic of Azerbaijan','Азербайджан','Азербайджанская Республика'],
        'flag': 'https://flagcdn.com/w320/az.png'
    },
    {
        'names': ['Morocco','Kingdom of Morocco','المغرب','المملكة المغربية','ⵍⵎⴰⵖⵔⵉⴱ','ⵜⴰⴳⵍⴷⵉⵜ ⵏ ⵍⵎⵖⵔⵉⴱ'],
        'flag': 'https://flagcdn.com/w320/ma.png'
    },
    {
        'names': ['Bulgaria','Republic of Bulgaria','България','Република България'],
        'flag': 'https://flagcdn.com/w320/bg.png'
    },
    {
        'names': ['Burundi','Republic of Burundi',"Republika y'Uburundi ",
    'République du Burundi','Uburundi'],
        'flag': 'https://flagcdn.com/w320/bi.png'
    },
    {
        'names': ['Uganda','Republic of Uganda'],
        'flag': 'https://flagcdn.com/w320/ug.png'
    },
    {
        'names': ['Kosovo','Kosova','Republic of Kosovo','Republika e Kosovës','Косово',
    'Република Косово'],
        'flag': 'https://flagcdn.com/w320/xk.png'
    },
    {
        'names': ['Mozambique','Moçambique','Republic of Mozambique',
    'República de Moçambique'],
        'flag': 'https://flagcdn.com/w320/mz.png'
    },
    {
        'names': ['Georgia','საქართველო'],
        'flag': 'https://flagcdn.com/w320/ge.png'
    },
    {
        'names': ['United Kingdom','UK','United Kingdom of Great Britain and Northern Ireland'],
        'flag': 'https://flagcdn.com/w320/gb.png'
    },
    {
        'names': ['Romania','România'],
        'flag': 'https://flagcdn.com/w320/ro.png'
    },
    {
        'names': ['Vietnam','Cộng hòa xã hội chủ nghĩa Việt Nam','Socialist Republic of Vietnam','Việt Nam'],
        'flag': 'https://flagcdn.com/w320/vn.png'
    },
    {
        'names': ['República Árabe Saharaui Democrática','Sahara Occidental','Sahrawi Arab Democratic Republic','Western Sahara','الجمهورية العربية الصحراوية الديمقراطية','الصحراء الغربية'],
        'flag': 'https://flagcdn.com/w320/eh.png'
    },
    {
        'names': ['Japan','日本'],
        'flag': 'https://flagcdn.com/w320/jp.png'
    },
    {
        'names': ['Egypt','Arab Republic of Egypt','جمهورية مصر العربية','مصر'],
        'flag': 'https://flagcdn.com/w320/eg.png'
    },
    {
        'names': ['Liberia','Republic of Liberia'],
        'flag': 'https://flagcdn.com/w320/lr.png'
    },
    {
        'names': ['Lithuania','Lietuva','Lietuvos Respublikos','Republic of Lithuania'],
        'flag': 'https://flagcdn.com/w320/lt.png'
    },
    {
        'names': ['Haiti','Ayiti','Haïti','Repiblik Ayiti','Republic of Haiti',
    "République d'Haïti"],
        'flag': 'https://flagcdn.com/w320/ht.png'
    },
    {
        'names': ['Papua New Guinea','Independen Stet bilong Papua Niugini','Independent State of Papua New Guinea','Papua Niu Gini','Papua Niugini'],
        'flag': 'https://flagcdn.com/w320/pg.png'
    },
    {
        'names': ['Kyrgyzstan','Kyrgyz Republic','Киргизия','Кыргыз Республикасы','Кыргызская Республика','Кыргызстан'],
        'flag': 'https://flagcdn.com/w320/kg.png'
    },
    {
        'names': ['Palau','Belau','Beluu er a Belau','Republic of Palau'],
        'flag': 'https://flagcdn.com/w320/pw.png'
    },
    {
        'names': ['Madagascar','Madagasikara',"Repoblikan'i Madagasikara",'Republic of Madagascar','République de Madagascar'],
        'flag': 'https://flagcdn.com/w320/mg.png'
    },
    {
        'names': ['Gambia','Republic of the Gambia'],
        'flag': 'https://flagcdn.com/w320/gm.png'
    },
    {
        'names': ['Togo','République togolaise','Togolese Republic'],
        'flag': 'https://flagcdn.com/w320/tg.png'
    },
    {
        'names': ['Slovenia','Republic of Slovenia','Republika Slovenija','Slovenija'],
        'flag': 'https://flagcdn.com/w320/si.png'
    },
    {
        'names': ['Singapore','Republic of Singapore','Republik Singapura','Singapura','சிங்கப்பூர்','சிங்கப்பூர் குடியரசு','新加坡','新加坡共和国'],
        'flag': 'https://flagcdn.com/w320/sg.png'
    },
    {
        'names': ['USA','US','United States','United States of America'],
        'flag': 'https://flagcdn.com/w320/us.png'
    },
    {
        'names': ['Malaysia','مليسيا'],
        'flag': 'https://flagcdn.com/w320/my.png'
    },
    {
        'names': ['Germany','Bundesrepublik Deutschland','Deutschland','Federal Republic of Germany'],
        'flag': 'https://flagcdn.com/w320/de.png'
    },
    {
        'names': ['Antigua and Barbuda'],
        'flag': 'https://flagcdn.com/w320/ag.png'
    },
    {
        'names': ['Somalia','Federal Republic of Somalia','Jamhuuriyadda Federaalka Soomaaliya','Soomaaliya','الصومال\u200e\u200e','جمهورية الصومال\u200e\u200e'],
        'flag': 'https://flagcdn.com/w320/so.png'
    },
    {
        'names': ['Albania','Republic of Albania','Republika e Shqipërisë','Shqipëria'],
        'flag': 'https://flagcdn.com/w320/al.png'
    },
    {
        'names': ['Dominica','Commonwealth of Dominica'],
        'flag': 'https://flagcdn.com/w320/dm.png'
    },
    {
        'names': ['Zambia','Republic of Zambia'],
        'flag': 'https://flagcdn.com/w320/zm.png'
    },
    {
        'names': ['Cook Islands',"Kūki 'Āirani"],
        'flag': 'https://flagcdn.com/w320/ck.png'
    },
    {
        'names': ['Guinea','Guinée','Republic of Guinea','République de Guinée'],
        'flag': 'https://flagcdn.com/w320/gn.png'
    },
    {
        'names': ['Comoros','Comores','Komori','Udzima wa Komori','Union des Comores','Union of the Comoros','الاتحاد القمري','القمر\u200e'],
        'flag': 'https://flagcdn.com/w320/km.png'
    },
    {
        'names': ['Niue','Niuē'],
        'flag': 'https://flagcdn.com/w320/nu.png'
    },
    {
        'names': ['Switzerland','Confederazione Svizzera','Confederaziun svizra','Confédération suisse','Schweiz','Schweizerische Eidgenossenschaft','Suisse','Svizra','Svizzera','Swiss Confederation'],
        'flag': 'https://flagcdn.com/w320/ch.png'
    },
    {
        'names': ['Sudan','Republic of the Sudan','السودان','جمهورية السودان'],
        'flag': 'https://flagcdn.com/w320/sd.png'
    },
    {
        'names': ['Tajikistan','Republic of Tajikistan','Республика Таджикистан','Таджикистан','Тоҷикистон','Ҷумҳурии Тоҷикистон'],
        'flag': 'https://flagcdn.com/w320/tj.png'
    },
    {
        'names': ['Uruguay','Oriental Republic of Uruguay','República Oriental del Uruguay'],
        'flag': 'https://flagcdn.com/w320/uy.png'
    },
    {
        'names': ['Cyprus','Kıbrıs','Kıbrıs Cumhuriyeti','Republic of Cyprus','Δημοκρατία της Κύπρος','Κύπρος'],
        'flag': 'https://flagcdn.com/w320/cy.png'
    }
]

async def check_flag_guess(message: discord.Message, parent, embed: discord.Embed) -> None:
    """Check if guess is right"""

    if embed.title != 'Which country is this? Reply to me.':
        return None
    if '#' not in embed.footer.text:
        return None
    try:
        country_id = int(embed.footer.text.replace('#', ''))
    except:
        return None
    
    country_id = country_id - 1

    country = countries[country_id]
    countrys_names = country['names']


    answered = False
    for name in countrys_names:
        if name.casefold() == message.content.casefold():
            answered = True
    
    if answered:
        await message.add_reaction(CHECK)
        await message.channel.send(content=f'You\'re right {message.author.nick}! It\'s {countrys_names[0]}.')
        embed.remove_footer()
        embed.set_footer(text=f'It was {countrys_names[0]}, answered by {message.author.nick}!')
        await parent.edit(embed=embed)
    else:
        answered = False
        await message.add_reaction(ERR)

    return countrys_names[0], answered

async def get_flag() -> Embed:
    # Get random country

    the_limit = 0

    while the_limit < 40:
        country_id = random.randint(0,len(countries))

        if country_id+1 in already_countries:
            the_limit += 1
        else:
            the_limit += 42

        country = countries[country_id]

    country_flag_url = country['flag']

    country_id = country_id+1

    already_countries.append(country_id)

    embed = Embed(
        title='Which country is this? Reply to me.',
        color=0X45c33a,
    )
    embed.set_image(url=country_flag_url)
    embed.set_footer(text=f'#{country_id}')

    return embed

