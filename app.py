from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_vin', methods=['POST'])
def check_vin():
    vin = request.form.get('vin')
    # 1. Get Technical Specs from NHTSA
    spec_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
    spec_data = requests.get(spec_url).json()['Results'][0]
    
    # 2. Get Recall History from NHTSA
    recall_url = f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={spec_data['Make']}&model={spec_data['Model']}&modelYear={spec_data['ModelYear']}"
    recall_data = requests.get(recall_url).json()

    return jsonify({
        "specs": spec_data,
        "recalls": recall_data['results'] if 'results' in recall_data else [],
        "history_link": f"https://www.vehiclehistory.com/vin-report/{vin}" # Free history mirror
    })

if __name__ == '__main__':
    app.run(debug=True)
