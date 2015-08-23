hospital_to_id_map = {
  'brand': 'a03F0000009FQ7V',
  'sbmc': 'a03F0000009Ev1c',
  'mmc': 'a03F0000009EvQQ',
  'CMMC': 'a03F0000009Ev1h',
  'NBI': 'a03F0000009Ev1S',
  'CMC': 'a03F0000009Ev1N',
  'KMC/Monmouth Medical Center, Southern Campus': 'a03F0000009Ev1X',
  'Hospice and Home Car': 'a03F0000009YdRH',
  'JCMC': 'a03F0000009buV7',
  'Rider University': 'a03F000000Ig4aW',
  'Pur Beverage': 'a03F000000If1eU',
  'Morristown Medical Center': 'a03F0000009Ev18',
  'Overlook Medical Center': 'a03F0000009Ev1m',
  'Newton Medical Center': 'a03F000000A9jXI',
  'Chilton Medical Center': 'a03F000000A9jXN',
  'Goryeb Children\'s Hospital': 'a03F000000A9jXS',
  'Atlantic Health Brand': 'a03F000000J29GR',
  'Robert Wood Johnson Brand': 'a03F000000Jm4t0'
}

barnabas_daily_keywords = [
  'BH 08 JCMC',
  'BH 00 EC 005845',
  'BH 00 Brand',
  'BH 01 SBMC',
  'BH 02 MMC',
  'BH 03 NBI',
  'BH 04 CMMC',
  'BH 05 KMC',
  'BH 06 CMC',
]

media_types = [
  { 'displayOrder': '1',
    'mediaTypeId': '1',
    'mediaTypeName': 'Blogs'},
  { 'displayOrder': '2',
    'mediaTypeId': '2',
    'mediaTypeName': 'Videos'},
  { 'displayOrder': '3',
    'mediaTypeId': '4',
    'mediaTypeName': 'Images'},
  { 'displayOrder': '4',
    'mediaTypeId': '5',
    'mediaTypeName': 'Mainstream News'},
  { 'displayOrder': '5',
    'mediaTypeId': '8',
    'mediaTypeName': 'Twitter'},
  { 'displayOrder': '6',
    'mediaTypeId': '10',
    'mediaTypeName': 'Forums'},
  { 'displayOrder': '7',
    'mediaTypeId': '9',
    'mediaTypeName': 'Forum Replies'},
  { 'displayOrder': '8',
    'mediaTypeId': '11',
    'mediaTypeName': 'Comments'},
  { 'displayOrder': '9',
    'mediaTypeId': '12',
    'mediaTypeName': 'Facebook'},
  { 'displayOrder': '10',
    'mediaTypeId': '13',
    'mediaTypeName': 'Aggregator'},
  { 'displayOrder': '11',
    'mediaTypeId': '14',
    'mediaTypeName': 'Buy/Sell'},
  { 'displayOrder': '13',
    'mediaTypeId': '16',
    'mediaTypeName': 'MySpace'}
]

report_media_type_names = ['Twitter', 'Facebook', 'MySpace', 'Comments', 'Images', 'Videos', 'Forums', 'Forum Replies']
report_media_types = list(filter(lambda mt: mt['mediaTypeName'] in report_media_type_names, media_types))
report_media_type_ids = list(map(lambda mt: mt['mediaTypeId'], report_media_types))

advanced_filter_types = [
  { 'name': 'Classificiation', 'typeId': '7'},
  { 'name': 'Topic Profile Sentiment Subjects', 'typeId': '11'},
  { 'name': 'Engagement Level', 'typeId': '4'},
  { 'name': 'Widget Keywords', 'typeId': '12'},
  { 'name': 'Keyword Group', 'typeId': '9'},
  { 'name': 'Language', 'typeId': '1'},
  { 'name': 'Media Type', 'typeId': '2'},
  { 'name': 'Media Type', 'typeId': '23'},
  { 'name': 'Post Tag', 'typeId': '6'},
  { 'name': 'Region', 'typeId': '0'},
  { 'name': 'Sentiment', 'typeId': '3'},
  { 'name': 'Source Tag', 'typeId': '5'},
  { 'name': 'User Assignment', 'typeId': '8'}
]
