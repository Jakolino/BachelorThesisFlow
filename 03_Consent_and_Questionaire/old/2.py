import json
import csv
from datetime import datetime
import os
from typing import Dict, Any, List

class DemographicsDataProcessor:
    """Process and store demographics questionnaire data"""
    
    def __init__(self, data_dir="demographics_data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def process_form_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw form data into structured JSON.
        
        Args:
            form_data: Dictionary with form field names and values
            
        Returns:
            Structured dictionary with processed data
        """
        
        # Create participant ID if not present
        if 'teilnehmer_id' not in form_data:
            form_data['teilnehmer_id'] = f"TN_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(2).hex()}"
        
        # Add processing timestamp
        form_data['processed_at'] = datetime.now().isoformat()
        
        # Handle special cases
        processed_data = {
            "metadata": {
                "participant_id": form_data.get('teilnehmer_id'),
                "submission_time": form_data.get('timestamp', datetime.now().isoformat()),
                "processed_time": form_data['processed_at'],
                "data_version": "1.0"
            },
            "demographics": {
                "personal": {
                    "age": self._safe_int(form_data.get('alter')),
                    "gender": form_data.get('geschlecht'),
                    "birthplace": form_data.get('geburtsort', '')
                },
                "education": {
                    "highest_degree": form_data.get('bildung'),
                    "occupation": form_data.get('beruf', ''),
                    "studied_math": form_data.get('mathe_studium', 'nein')
                },
                "language": {
                    "native_language": form_data.get('muttersprache'),
                    "german_level": form_data.get('deutsch_niveau', 'muttersprache')
                },
                "handedness": form_data.get('haendigkeit', 'rechts'),
                "health": {
                    "impairments": self._process_impairments(form_data.get('beeintraechtigung', [])),
                    "notes": form_data.get('bemerkungen', '')
                }
            },
            "consent": {
                "agreed": form_data.get('einwilligung') == 'on' or form_data.get('einwilligung') == True,
                "consent_date": datetime.now().isoformat()
            }
        }
        
        return processed_data
    
    def _safe_int(self, value, default=None):
        """Safely convert to integer"""
        try:
            return int(value) if value else default
        except (ValueError, TypeError):
            return default
    
    def _process_impairments(self, impairment_data):
        """Process impairment information"""
        if isinstance(impairment_data, list):
            return {
                "visual": 'ja_sehen' in impairment_data,
                "auditory": 'ja_hoeren' in impairment_data,
                "both": 'ja_beides' in impairment_data,
                "none": 'nein' in impairment_data
            }
        else:
            return {
                "visual": impairment_data == 'ja_sehen',
                "auditory": impairment_data == 'ja_hoeren',
                "both": impairment_data == 'ja_beides',
                "none": impairment_data == 'nein'
            }
    
    def save_as_json(self, data: Dict[str, Any], filename: str = None) -> str:
        """
        Save processed data as JSON file.
        
        Returns:
            Path to saved file
        """
        if not filename:
            participant_id = data['metadata']['participant_id']
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"demographics_{participant_id}_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Data saved to {filepath}")
        return filepath
    
    def save_as_csv_row(self, data: Dict[str, Any], csv_file: str = "all_participants.csv"):
        """
        Append data to CSV file for easy analysis.
        """
        # Flatten the nested structure for CSV
        flat_data = {
            'participant_id': data['metadata']['participant_id'],
            'submission_time': data['metadata']['submission_time'],
            'age': data['demographics']['personal']['age'],
            'gender': data['demographics']['personal']['gender'],
            'birthplace': data['demographics']['personal']['birthplace'],
            'education': data['demographics']['education']['highest_degree'],
            'occupation': data['demographics']['education']['occupation'],
            'studied_math': data['demographics']['education']['studied_math'],
            'native_language': data['demographics']['language']['native_language'],
            'german_level': data['demographics']['language']['german_level'],
            'handedness': data['demographics']['handedness'],
            'visual_impairment': data['demographics']['health']['impairments']['visual'],
            'auditory_impairment': data['demographics']['health']['impairments']['auditory'],
            'both_impairments': data['demographics']['health']['impairments']['both'],
            'no_impairments': data['demographics']['health']['impairments']['none'],
            'notes': data['demographics']['health']['notes'],
            'consent': data['consent']['agreed']
        }
        
        csv_path = os.path.join(self.data_dir, csv_file)
        file_exists = os.path.isfile(csv_path)
        
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=flat_data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(flat_data)
        
        print(f"Data appended to {csv_path}")
        return csv_path
    
    def load_json_file(self, filepath: str) -> Dict[str, Any]:
        """Load JSON data from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def batch_process_files(self, input_dir: str, pattern: str = "*.json"):
        """Process multiple JSON files"""
        import glob
        
        json_files = glob.glob(os.path.join(input_dir, pattern))
        all_data = []
        
        for filepath in json_files:
            try:
                data = self.load_json_file(filepath)
                all_data.append(data)
                print(f"Loaded {filepath}")
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        
        return all_data

# Example usage
def process_submitted_data_example():
    """Example of how to use the processor"""
    
    # Simulate form data from HTML submission
    sample_form_data = {
        'alter': '28',
        'geschlecht': 'weiblich',
        'geburtsort': 'München',
        'bildung': 'master',
        'beruf': 'Doktorandin',
        'mathe_studium': 'ja',
        'muttersprache': 'Deutsch',
        'deutsch_niveau': 'muttersprache',
        'haendigkeit': 'rechts',
        'beeintraechtigung': 'nein',
        'bemerkungen': 'Keine besonderen Anmerkungen',
        'einwilligung': 'on',
        'teilnehmer_id': 'TN_001',
        'timestamp': datetime.now().isoformat()
    }
    
    # Initialize processor
    processor = DemographicsDataProcessor(data_dir="studien_daten")
    
    # Process the data
    processed = processor.process_form_data(sample_form_data)
    
    # Save as JSON
    json_path = processor.save_as_json(processed)
    
    # Append to CSV
    csv_path = processor.save_as_csv_row(processed)
    
    print(f"\nProcessed data structure:")
    print(json.dumps(processed, indent=2, ensure_ascii=False))
    
    return processed

# Option 3: Parse HTML directly and create empty template
def create_empty_json_template(html_file_path: str, output_path: str = "demographics_template.json"):
    """
    Create an empty JSON template based on HTML form structure.
    Useful for creating data entry templates.
    """
    
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find all form fields with their labels
    template = {
        "metadata": {
            "template_version": "1.0",
            "created": datetime.now().isoformat(),
            "description": "Demographics questionnaire data template"
        },
        "participant_data": {}
    }
    
    # Extract field names and create empty structure
    field_pattern = r'name=["\']([^"\']*)["\']'
    fields = set(re.findall(field_pattern, html))
    
    # Create empty structure for each field
    for field in fields:
        if field in ['einwilligung']:
            template["participant_data"][field] = False
        elif field in ['alter']:
            template["participant_data"][field] = None
        else:
            template["participant_data"][field] = ""
    
    template["participant_data"]["timestamp"] = ""
    
    # Save template
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"Template saved to {output_path}")
    return template

if __name__ == "__main__":
    # Example: Process a single submission
    processed_data = process_submitted_data_example()
    
    # Example: Create template from HTML
    create_empty_json_template("demographics_questionnaire.html")
    
    print("\nSetup complete! Data will be saved to 'studien_daten/' directory")