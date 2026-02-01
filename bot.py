import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def get_news():
    # Haber kaynakları ve konular (Siber Güvenlik, Yapay Zeka, Yazılım)
    url = "https://news.ycombinator.com/" # Hacker News örneği
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Haberleri çek
    articles = soup.find_all('span', class_='titleline', limit=15)
    
    # İlgilendiğin anahtar kelimeler
    keywords = ['AI', 'Cyber', 'Security', 'Software', 'Python', 'C#', 'Hack']
    found_news = []
    
    for article in articles:
        text = article.text
        if any(key.lower() in text.lower() for key in keywords):
            found_news.append(text)
            if len(found_news) == 3: break # En fazla 3 haber al

    # Dosyaya kaydet
    date_str = datetime.now().strftime('%Y-%m-%d')
    content = f"--- {date_str} Teknoloji Haberleri ---\n"
    content += "\n".join(found_news) if found_news else "Bugün özel bir haber bulunamadı."
    
    # Logs klasörü yoksa oluştur
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    with open(f"logs/news_{date_str}.txt", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    get_news()
