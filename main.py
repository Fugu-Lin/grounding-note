from service.grounding_search_service import GroundingSearchService
from service.query_rewrite_service    import QueryRewriteService
from service.summary_service          import SummaryService
from service.generate_title_service   import GenerateTitleService
from flask import Flask, request, jsonify, render_template_string
from google.cloud import storage
import markdown
import os

app = Flask(__name__)

@app.route('/<path:blob_name>', methods=['GET'])
def display_markdown(blob_name):
    bucket_name = 'grounding-bucket'
    print(blob_name)
    
    try:
        markdown_content = get_markdown_from_gcs(bucket_name, blob_name)
    except Exception as e:
        return f"Error fetching markdown content: {str(e)}", 500

    html_content = markdown.markdown(markdown_content)

    template = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Markdown Display</title>
      </head>
      <body>
        <div class="container">
          {{ content|safe }}
        </div>
      </body>
    </html>
    '''
    
    print("template", template)
    print("html_content", html_content)
    return render_template_string(template, content=html_content)

@app.route('/generate_new_article', methods=['POST'])
def generate_new_article():

    groundingSearchService = GroundingSearchService()
    queryRewriteService    = QueryRewriteService()
    summaryService         = SummaryService()
    generateTitleService   = GenerateTitleService()
    
    request_data = request.get_json()
    query        = request_data.get('query')
    search_keywords      = queryRewriteService.process(query)
    disorganized_content = groundingSearchService.process(search_keywords)
    summarized_article_content = summaryService.process(disorganized_content)
    title = generateTitleService.process(summarized_article_content)
    
    if not summarized_article_content:
        return jsonify({"error": "No markdown content provided"}), 400
    
    bucket_name = 'grounding-bucket'
    blob_name = f'{title}.md'
    
    # Define the path for the markdown file in GCS
    gcs_path = f"gs://{bucket_name}/{blob_name}"
    
    # Upload the markdown content to GCS
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(summarized_article_content, content_type='text/markdown')
    
    # Define the Cloud Run IP
    cloud_run_ip = 'https://markdown-test-pkgegxonya-de.a.run.app'
    
    # Return the Cloud Run IP + GCS path
    response_data = {
        "url": f"{cloud_run_ip}/{blob_name}"
    }
    
    return jsonify(response_data), 200

def get_markdown_from_gcs(bucket_name, blob_name):
    """Fetches a markdown file from GCS and returns its content."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.download_as_text()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)