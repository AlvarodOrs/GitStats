from utils.tools import load_config
from workers import retriever
def main():
    config = load_config()
    fetcher = retriever.fetch_data(config) #Outputs the entire json
    

if __name__ == '__main__':
    main()