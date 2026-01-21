
def make_activity_card():    
    with open('generators/models/svg/activity.svg', 'r', encoding='utf-8') as file: activity_svg = file.read()

    with open(f'generators/models/{}/'): 
    return activity_svg

if __name__ == '__main__':
    print(make_activity_card())