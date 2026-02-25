import io
import requests
from flask import Flask, render_template, request, jsonify, send_file
from fpdf import FPDF

app = Flask(__name__)

# Helper to talk to the NHTSA Government API
def get_nhtsa_data(vin):
    headers = {'User-Agent': 'VinnyCheck/1.0'}
    try:
        # Get Specs
        spec_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
        specs = requests.get(spec_url, headers=headers, timeout=10).json()['Results'][0]
        
        # Get Recalls (Using Make/Model/Year from the specs we just got)
        make = specs.get('Make')
        model = specs.get('Model')
        year = specs.get('ModelYear')
        
        recall_url = f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={make}&model={model}&modelYear={year}"
        recalls = requests.get(recall_url, headers=headers, timeout=10).json()
        
        return specs, recalls.get('results', [])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_vin', methods=['POST'])
def check_vin():
    vin = request.form.get('vin', '').strip().upper()
    if not vin:
        return jsonify({"error": "No VIN provided"}), 400

    specs, recalls = get_nhtsa_data(vin)
    
    if not specs:
        return jsonify({"error": "Could not fetch data"}), 500

    return jsonify({
        "specs": specs,
        "recalls": recalls,
        "history_link": f"https://www.vehiclehistory.com/vin-report/{vin}"
    })

@app.route('/download_pdf/<vin>')
def download_pdf(vin):
    specs, recalls = get_nhtsa_data(vin)
    
    # PDF Generation
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 15, "VINNY VEHICLE REPORT", ln=True, align='C')
    pdf.set_font("Helvetica", '', 10)
    pdf.cell(0, 10, f"VIN: {vin}", ln=True, align='C')
    pdf.ln(10)
    
    # Data Table
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", 'B', 12)
    
    important_fields = [
        ("Year", "ModelYear"), ("Make", "Make"), ("Model", "Model"),
        ("Trim", "Trim"), ("Engine", "DisplacementL"), ("Cylinders", "EngineCylinders"),
        ("Drive Type", "DriveType"), ("Body Class", "BodyClass")
    ]
    
    for label, key in important_fields:
        pdf.cell(50, 10, label, border=1, fill=True)
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(140, 10, str(specs.get(key, "N/A")), border=1, ln=True)
        pdf.set_font("Helvetica", 'B', 12)

    # Recalls Section
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"Safety Recalls Found: {len(recalls)}", ln=True)
    
    # Save to memory buffer
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_bytes)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Vinny_Report_{vin}.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
