import hashlib


def create_id(metadata):
    unique_string = str(f"{metadata['file_size_bytes']}_{metadata['created_at']}")
    unique_id = hashlib.md5(unique_string.encode()).hexdigest()
    metadata['unique_id'] = unique_id
    return metadata