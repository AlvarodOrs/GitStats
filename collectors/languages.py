def get_percentages(total_list:list):

    total = sum(total_list.values())
    return {
        lang: bits/total*100
        for lang, bits in total_list.items()
        }