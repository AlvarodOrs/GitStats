def get_percentages(total_list: list):
    input(total_list)
    total = sum(total_list.values())
    langs = {
        lang: bits/total*100
        for lang, bits in total_list.items()
        }
    
    return sorted(langs.items(), key=lambda item: item[1], reverse=True)