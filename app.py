from flask import Flask, render_template_string, request

app = Flask(__name__)

NOM_BOUTIQUE = "DI_WIZ SHOP"

produits = {
    "t-shirt": 15,
    "chaussures": 35,
    "pantalon": 25,
    "casquette": 10
}

commandes = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ boutique }}</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f2f2;
            padding: 15px;
        }

        .container {
            max-width: 500px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 15px;
        }

        h1 {
            text-align: center;
        }

        .chat {
            background: #eeeeee;
            padding: 15px;
            min-height: 200px;
            border-radius: 10px;
            margin-bottom: 15px;
        }

        input {
            width: 100%;
            padding: 12px;
            margin: 6px 0;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 8px;
        }

        button {
            width: 100%;
            padding: 12px;
            margin-top: 8px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }

        .formulaire {
            display: none;
            margin-top: 20px;
            background: #f7f7f7;
            padding: 15px;
            border-radius: 10px;
        }
    </style>

    <script>
        function afficherCommande() {
            var formulaire = document.getElementById("formulaire");

            if (formulaire.style.display === "none") {
                formulaire.style.display = "block";
            } else {
                formulaire.style.display = "none";
            }
        }
    </script>
</head>

<body>

<div class="container">

    <h1>🤖 {{ boutique }}</h1>

    <div class="chat">

        {% if message %}
            <p><b>Client :</b> {{ message }}</p>
            <p><b>Bot :</b> {{ reponse|safe }}</p>
        {% else %}
            <p><b>Bot :</b> Bonjour 👋 Bienvenue chez {{ boutique }} !</p>
            <p>Écris <b>catalogue</b> pour voir nos produits.</p>
        {% endif %}

    </div>

    <form method="POST">

        <input
            type="text"
            name="message"
            placeholder="Écris ton message..."
            required
        >

        <button type="submit">
            💬 Envoyer
        </button>

    </form>

    <button onclick="afficherCommande()">
        🛒 Commander
    </button>

    <div id="formulaire" class="formulaire">

        <h3>🛒 Nouvelle commande</h3>

        <form method="POST">

            <input
                type="hidden"
                name="action"
                value="commande"
            >

            <input
                type="text"
                name="nom"
                placeholder="Votre nom"
                required
            >

            <input
                type="text"
                name="produit"
                placeholder="Produit"
                required
            >

            <input
                type="number"
                name="quantite"
                placeholder="Quantité"
                min="1"
                required
            >

            <input
                type="text"
                name="telephone"
                placeholder="Téléphone"
                required
            >

            <button type="submit">
                ✅ Enregistrer la commande
            </button>

        </form>

    </div>

</div>

</body>
</html>
"""


def repondre(message):

    message = message.lower().strip()

    if "bonjour" in message or "salut" in message:
        return f"Bonjour 👋 Bienvenue chez {NOM_BOUTIQUE} !"

    elif "catalogue" in message or "produits" in message:
        texte = "🛍️ <b>Notre catalogue :</b><br><br>"

        for produit, prix in produits.items():
            texte += f"• {produit} : {prix}$<br>"

        return texte

    elif "t-shirt" in message:
        return f"Le t-shirt coûte {produits['t-shirt']} $."

    elif "chaussures" in message:
        return f"Les chaussures coûtent {produits['chaussures']} $."

    elif "pantalon" in message:
        return f"Le pantalon coûte {produits['pantalon']} $."

    elif "casquette" in message:
        return f"La casquette coûte {produits['casquette']} $."

    elif "livraison" in message:
        return "🚚 Oui, nous faisons des livraisons."

    elif "merci" in message:
        return "Avec plaisir 😊"

    else:
        return (
            "Je n'ai pas compris. "
            "Écris « catalogue » pour voir nos produits."
        )


@app.route("/", methods=["GET", "POST"])
def accueil():

    message = ""
    reponse = ""

    if request.method == "POST":

        if request.form.get("action") == "commande":

            nom = request.form.get("nom")
            produit = request.form.get("produit")
            quantite = request.form.get("quantite")
            telephone = request.form.get("telephone")

            commandes.append({
                "nom": nom,
                "produit": produit,
                "quantite": quantite,
                "telephone": telephone
            })

            message = "Commande"
            reponse = "✅ Merci ! Votre commande a été enregistrée."

        else:

            message = request.form.get("message", "")
            reponse = repondre(message)

    return render_template_string(
        HTML,
        boutique=NOM_BOUTIQUE,
        message=message,
        reponse=reponse
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
