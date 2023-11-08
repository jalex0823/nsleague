# from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

@app.route('/api/v1.0/predictions', methods=['GET'])
def get_predictions():
    try:
        # Get the URL from the request parameters
        url = request.args.get('url')

        # Check if the URL is provided
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400

        # Validate the URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return jsonify({"error": "Invalid URL"}), 400

        # Get the User-Agent header from the request
        user_agent = request.headers.get('User-Agent')

        # Set headers including User-Agent and Referer to mimic a web browser request
        headers = {
            'User-Agent': user_agent if user_agent else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
            'Referer': parsed_url.scheme + '://' + parsed_url.netloc
        }

        # Make the request with the specified headers
        page = requests.get(url, headers=headers)

        # Check if the request was successful
        page.raise_for_status()

        soup = BeautifulSoup(page.content, 'html.parser')

        # List of HTML tags to search for
        tags_to_search = ['div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td', 'th', 'a', 'b', 'i', 'u', 'em', 'strong', 'small', 'big', 'strike', 'sub', 'sup', 'mark', 'code', 'pre', 'q', 'samp', 'kbd', 'var', 'cite', 'dfn', 'abbr', 'acronym', 'address', 'bdo', 'blo', 'ins']

        # List of classes that might contain predictions
        prediction_classes = ['ssg-scm', 'offer', 'ssg-scm-loaded']

        # List of titles that might contain predictions
        prediction_titles = ['predictions', 'picks', 'winner', 'losser', 'spread', 'over-under', 'over-under-picks', 'over-under-predictions', 'over-under-prediction']

        predictions = []

        # Search by tag
        for tag_to_search in tags_to_search:
            prediction_elems = soup.find_all(tag_to_search, class_=prediction_classes)
            predictions.extend([prediction_elem.text.strip() for prediction_elem in prediction_elems])

        # Search by title
        for prediction_title in prediction_titles:
            result = soup.find('div', {'title': prediction_title})
            if result:
                predictions.append(result.text.strip())

        if predictions:
            return jsonify(predictions)
        else:
            return jsonify({"error": "No predictions found", "html_content": str(page.content)}), 404  # Return 404 for not found

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error in request: {str(e)}")
        return jsonify({"error": "Failed to retrieve predictions", "exception": str(e)}), 403  # Return 403 for HTTP error

    except requests.exceptions.RequestException as e:
        logging.error(f"Error in request: {str(e)}")
        return jsonify({"error": "Failed to retrieve predictions", "exception": str(e)}), 500  # Return 500 for other request errors

if __name__ == '__main__':
    app.run(debug=True, port=5002)
requirements.txt

