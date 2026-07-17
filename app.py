import json
import os
import uuid
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

PACOTES = {
    "seguidores": [
        {"quantidade": "100", "preco": "10,90", "popular": False},
        {"quantidade": "500", "preco": "19,90", "popular": False},
        {"quantidade": "1.000", "preco": "29,90", "popular": True},
        {"quantidade": "2.000", "preco": "49,90", "popular": False},
        {"quantidade": "5.000", "preco": "99,90", "popular": False},
        {"quantidade": "10.000", "preco": "179,90", "popular": False},
    ],
    "curtidas": [
        {"quantidade": "100", "preco": "2,90", "popular": False},
        {"quantidade": "500", "preco": "4,90", "popular": False},
        {"quantidade": "1.000", "preco": "9,90", "popular": True},
        {"quantidade": "2.000", "preco": "18,90", "popular": False},
        {"quantidade": "4.000", "preco": "37,90", "popular": False},
        {"quantidade": "8.000", "preco": "65,90", "popular": False},
    ],
    "visualizacoes": [
        {"quantidade": "1.000", "preco": "7,90", "popular": False},
        {"quantidade": "5.000", "preco": "24,90", "popular": False},
        {"quantidade": "10.000", "preco": "39,90", "popular": True},
        {"quantidade": "25.000", "preco": "79,90", "popular": False},
        {"quantidade": "50.000", "preco": "139,90", "popular": False},
        {"quantidade": "100.000", "preco": "249,90", "popular": False},
    ],
}

VANTAGENS = [
    {"titulo": "Autoridade", "descricao": "Nosso principal objetivo e gerar resultados para voce! Por isso somos diferentes."},
    {"titulo": "Oportunidades", "descricao": "Pode ter certeza que voce tera uma experiencia excelente com nosso suporte."},
    {"titulo": "Prova Social", "descricao": "Cadastre-se e faca sua primeira compra em menos de 56 segundos."},
    {"titulo": "Confianca", "descricao": "Sua rede social e turbinada ou seu dinheiro de volta."},
    {"titulo": "Networking", "descricao": "Todas as compras realizadas sao totalmente sigilosas. Garantia de reembolso inclusa."},
    {"titulo": "Entrega Rapida", "descricao": "Seu pedido comeca a ser processado imediatamente apos a confirmacao do pagamento."},
]

FAQS = [
    {"pergunta": "E seguro comprar seguidores?", "resposta": "Sim. Nosso sistema utiliza distribuicao gradual e simulacao de comportamento organico, tornando o crescimento indetectavel pelos algoritmos do Instagram."},
    {"pergunta": "Quanto tempo leva a entrega?", "resposta": "A entrega e iniciada instantaneamente apos a confirmacao do pagamento. O volume total e distribuido ao longo de algumas horas para maxima seguranca."},
    {"pergunta": "Preciso fornecer minha senha?", "resposta": "Nunca. Precisamos apenas do seu @username publico. Seus dados de acesso permanecem exclusivamente com voce."},
    {"pergunta": "Os seguidores caem depois?", "resposta": "Oferecemos garantia de reposicao de 30 dias. Caso haja qualquer reducao, nosso sistema repoe automaticamente sem custo adicional."},
    {"pergunta": "Quais formas de pagamento sao aceitas?", "resposta": "Aceitamos PIX, cartao de credito e boleto bancario. Pagamentos via PIX sao processados instantaneamente."},
]


def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(ORDERS_FILE):
        save_json(ORDERS_FILE, [])


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    return render_template(
        "index.html",
        pacotes=PACOTES,
        vantagens=VANTAGENS,
        faqs=FAQS,
    )


@app.route("/comprar", methods=["POST"])
def comprar():
    categoria = request.form.get("categoria", "")
    quantidade = request.form.get("quantidade", "")
    preco = request.form.get("preco", "")
    instagram = request.form.get("instagram", "").strip()
    telefone = request.form.get("telefone", "").strip()
    email = request.form.get("email", "").strip()

    if not all([instagram, telefone, email]):
        return redirect(url_for("index"))

    orders = load_json(ORDERS_FILE)
    order = {
        "id": str(uuid.uuid4()),
        "categoria": categoria,
        "quantidade": quantidade,
        "preco": preco,
        "instagram": instagram,
        "telefone": telefone,
        "email": email,
        "status": "pendente",
        "date": datetime.now().isoformat(),
    }
    orders.append(order)
    save_json(ORDERS_FILE, orders)

    return render_template("checkout.html", order=order)


if __name__ == "__main__":
    ensure_data_files()
    app.run(debug=True, port=5000)
