from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_function():
    data = request.json
    # Burada Python fonksiyonunuzu çağırabilirsiniz
    result = your_python_function(data)
    return jsonify({'result': result})

def your_python_function(data):
    # Python fonksiyonunuzun mantığı
    return "Fonksiyon çalıştırıldı, veri: "

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
