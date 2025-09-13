from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db = {
    'host': 'localhost',
    'port': '3307',
    'user': 'root',
    'password': 'admon',
    'database': 'producto',
    'collation': 'utf8mb4_general_ci'
}

@app.route('/verificar_stock', methods=['GET'])
def verificar_stock():
    producto_id = request.args.get('producto_id')
    cantidad_solicitada = request.args.get('cantidad')

    if not producto_id or not cantidad_solicitada:
        return jsonify({"disponible": False, "mensaje": "Faltan parámetros"}), 400

    try:
        cantidad_solicitada = int(cantidad_solicitada)
    except ValueError:
        return jsonify({"disponible": False, "mensaje": "Cantidad inválida"}), 400

    conn = mysql.connector.connect(**db)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT stock FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    if producto:
        if producto['stock'] >= cantidad_solicitada:
            return jsonify({"disponible": True, "mensaje": "Stock suficiente"}), 200
        else:
            return jsonify({"disponible": False, "mensaje": "Stock insuficiente"}), 200
    else:
        return jsonify({"disponible": False, "mensaje": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
