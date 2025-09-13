from flask import Flask, jsonify, request
import osa

app = Flask(__name__)

url_wsdl = 'https://www.banguat.gob.gt/variables/ws/TipoCambio.asmx?WSDL'

client = osa.Client(url_wsdl)

@app.route('/tipo_cambio_dia', methods=['GET'])
def tipo_cambio_dia():
    try:
        response = client.service.TipoCambioDia()
        resultado = {
            "fecha": response.CambioDolar.VarDolar[0].fecha,
            "referencia": response.CambioDolar.VarDolar[0].referencia
        }
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener tipo de cambio del día: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
