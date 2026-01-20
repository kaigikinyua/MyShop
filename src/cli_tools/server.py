from flask import Flask, jsonify, request

app = Flask(__name__)

items = [{"id": 1, "name": "item 1"}, {"id": 2, "name": "item 2"}]

@app.route('/api/items', methods=['GET'])
def get_items():
    print("Get request")
    return jsonify(items)

@app.route('/api/items', methods=['POST'])
def create_item():
    print('Post request')
    new_item = {"id": len(items) + 1, "name": request.json.get('data')}
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == "__main__":
    app.run(debug=True)