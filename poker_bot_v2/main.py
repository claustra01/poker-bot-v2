import os
from dotenv import load_dotenv

def main():
    
    load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
    TOKEN = os.environ['DISCORD_BOT_TOKEN']
    
    print(TOKEN)

if __name__ == '__main__':
    main()