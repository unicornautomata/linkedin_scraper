from flask import Flask, request, jsonify
from googlesearch import search

app = Flask(__name__)

def get_linkedin_profile(name, company):
    query = f'site:linkedin.com/in/ AND "{name}" AND "{company}"'
    search_results = search(query, num_results=10)
    linkedin_links = [url for url in search_results if "linkedin.com/in/" in url]
    if linkedin_links:
        return linkedin_links[0]
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
