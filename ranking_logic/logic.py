from ranking_logic.text_decoding import Hostile_list, Less_hostile_list
import hashlib


def adding_fields(metadata):
    metadata = create_id(metadata)

    metadata['is_bds'] = False
    metadata['bds_threat_level'] = 'none'

    l = len(metadata['text'].split(' '))
    n = (metadata['score'] / l) * 100
    metadata['bds_percent'] = n

    if metadata['bds_percent'] > 10:
        metadata['is_bds'] = True

    if metadata['bds_percent'] > 10 and metadata['bds_percent'] < 20:
        metadata['bds_threat_level'] = 'medium'
    elif metadata['bds_percent'] > 20:
        metadata['bds_threat_level'] = 'high'

    return metadata



def scored_text(metadata):
    score = 0
    text = metadata['text'].lower()
    for item in Hostile_list:
        if item.lower() in text:
            score += text.count(item.lower()) * 10

    for item in Less_hostile_list:
        if item in text:
            score += text.count(item.lower()) * 5

    metadata['score'] = score
    metadata = adding_fields(metadata)

    return metadata


def create_id(metadata):
    unique_string = str(f"{metadata['file_size_bytes']}_{metadata['created_at']}")
    unique_id = hashlib.md5(unique_string.encode()).hexdigest()
    metadata['unique_id'] = unique_id
    return metadata