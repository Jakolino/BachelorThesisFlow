from flask import Flask, request, jsonify, render_template
import json
from datetime import datetime
import os

app = Flask(__name__)
processor = DemographicsDataProcessor()

@app.route('/')
def index():
    """Serve the HTML form"""
    return render_template('demographics_questionnaire.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    """Handle form submission"""
    try:
        # Get form data
        form_data = request.form.to_dict()
        
        # Process the data
        processed = processor.process_form_data(form_data)
        
        # Save as JSON
        json_path = processor.save_as_json(processed)
        
        # Append to CSV
        csv_path = processor.save_as_csv_row(processed)
        
        return jsonify({
            'success': True,
            'message': 'Data saved successfully',
            'participant_id': processed['metadata']['participant_id'],
            'json_file': json_path,
            'csv_file': csv_path
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/data/<participant_id>', methods=['GET'])
def get_participant_data(participant_id):
    """Retrieve participant data"""
    try:
        # Find file with matching participant_id
        data_dir = "demographics_data"
        for filename in os.listdir(data_dir):
            if participant_id in filename and filename.endswith('.json'):
                filepath = os.path.join(data_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return jsonify(data), 200
        
        return jsonify({'error': 'Participant not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)