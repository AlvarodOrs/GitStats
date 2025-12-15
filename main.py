from utils.tools import load_config
from workers import retriever
from svg_tool import image_maker

def main():
    config = load_config()
    data = retriever.fetch_data(config) #Outputs the entire json
    #data = load_config('data/full_github_stats.json')
    image_maker.image_maker(data)

if __name__ == '__main__':
    main()