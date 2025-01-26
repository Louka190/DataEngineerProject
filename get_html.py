import requests

url = "https://kworb.net/spotify/country/gb_weekly.html"
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text  
    
    with open("weekly.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print("Le fichier HTML a été sauvegardé sous le nom 'weekly.html'.")
else:
    print(f"Erreur : {response.status_code}")

# curl https://www.olympedia.org/results/19000014 -o link.html