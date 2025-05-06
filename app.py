from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'AIzaSyAauNezGIq4pomGCGkPw2ACFb-h3VakTy0'        # Replace with your Google API key
CSE_ID = 'c1a53408d168f4ea8'    # Your public CSE ID

def get_linkedin_profile(name, company):
    query = f'linkedin.com {name} {company}'
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': API_KEY,
        'cx': CSE_ID,
        'q': query,
        'num': 10
    }

    response = requests.get(url, params=params)
    results = response.json()

    if 'items' not in results:
        return None

    linkedin_links = [item['link'] for item in results['items'] if "linkedin.com/in/" in item['link']]

    if linkedin_links:
        return linkedin_links[0]  # Return first LinkedIn profile link
    else:
        return None

@app.route('/find_linkedin', methods=['GET'])
def find_linkedin():
    name = request.args.get('name')
    company = request.args.get('company')

    if not name or not company:
        return jsonify({"error": "Missing 'name' or 'company' query parameter."}), 400

    linkedin_url = get_linkedin_profile(name, company)

    if linkedin_url:
        return jsonify({"linkedin_profile": linkedin_url})
    else:
        return jsonify({"message": "No LinkedIn profile found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
