from ranking_logic.text_decoding import Hostile_list, Less_hostile_list


def scored_text(text):
    score = 0
    text = text.lower()
    for item in Hostile_list:
        if item.lower() in text:
            score += text.count(item.lower()) * 10

    for item in Less_hostile_list:
        if item in text:
            score += text.count(item.lower()) * 5

    return score
