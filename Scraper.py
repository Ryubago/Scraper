import requests
from bs4 import BeautifulSoup
import smtplib
import time

# variable prenant en compte l'url du produit du site (ici une maquette)
URL = 'https://riseofgunpla.com/boutique/mg-1-100-gundam-kyrios'

# variable de simulation d'utilisateur (comme un bot)
sHeaders = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}

# fonction permettant de trouver le titre et le prix du produit
def check_price():
    page = requests.get(URL, headers=sHeaders)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # retrouver le titre dans la balise <h1>
    title = soup.find('h1')
    # si le titre a été récupéré
    if title:
        # afficher le titre
        print(title.get_text())
    
    # Recherche de l'élément <p> avec la classe "price"
    price_span = soup.find("p", class_="price")

    if price_span:
        # Recherche de l'élément <bdi> à l'intérieur de <p>
        bdi = price_span.find("bdi")
        # si le <bdi> a été trouvé
        if bdi:
            # afficher le prix
            print("Prix :", bdi.text.split())
        else:
            print("Élément <bdi> non trouvé.")
    else:
        print("Élément <span> non trouvé.")

    # convertir le <bdi>, qui est de type str en type list
    bdi_price = bdi.text.split()
    bdi_list = [char for item in bdi_price for char in item]
    # enlever le caractère virgule
    bdi_list.pop(2)
    # enlever le caractère €
    bdi_list.pop(-1)
    # reconvertir la liste en str
    bdi_prix_str = ''.join(bdi_list)
    # indiquer au programme que tous les caractères sont des entiers
    bdi_prix_int = int(bdi_prix_str)

    # fonction secondaire qui envoie un mail à une adresse email
    def send_mail():
        # appeler le serveur avec le module smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        # nécéssaire pour se connecter au serveur
        server.login('adresse email de réception', "mot de passe d'application google associé à l'adresse email de réception")

        # définir le message
        subject = 'Le prix a changé !'
        body = 'Regardez le lien : https://riseofgunpla.com/boutique/mg-1-100-gundam-kyrios'
        msg = f"Subject : {subject}\n\n{body}"
        msg = msg.encode('utf-8')

        # envoyer le message
        server.sendmail("adresse email qui enverra automatiquement le mail", 'adresse email de réception', msg)

        print('Vous avez reçu un email !')

        # rompre la connexion avec le serveur pendant un certain délai (voir plus bas)
        server.quit()

    # si le prix est inférieur à 65€
    if bdi_prix_int < 6500:
        # envoyer un email
        send_mail()
    # si le prix est supérieur à 65€
    if bdi_prix_int > 6500:
        # envoyer un email
        send_mail()
        
# définnir la durée entre 2 requêtes pour ne pas surcharger le serveur (ici 6h)
while(True):
    check_price()
    time.sleep(21600)

