from flask import Flask, request, jsonify, Response, redirect, url_for
import json
import random
import re
from urllib.parse import urlparse
import time

app = Flask(__name__)

# Hidden parameters
HIDDEN_PARAMS = {
    'home_samx': 'value_x',
    'home_same': 'value_e',
    'a_a': 'test_a',
    'a_b': 'test_b',
    'secret_key': 'hidden_value',
    'user_id': '12345',
    'admin_token': 'super_secret_789'
}

# Sensitive headers
SENSITIVE_HEADERS = {
    'User-Agent': ['CustomAgent/1.0', 'TestBot'],
    'X-Forwarded-For': ['192.168.1.1'],
    'Referer': ['https://evil.com'],
    'Authorization': ['Bearer secret_token']
}

# List of random responses for your_id parameter
RANDOM_RESPONSES = [
    "ID processed successfully!",
    "Your ID has been verified!",
    "Random ID check completed!",
    "ID validation in progress...",
    "Unique ID detected!"
]

@app.route('/', methods=['GET', 'POST'])
@app.route('/x/', methods=['GET', 'POST'])
@app.route('/a/', methods=['GET', 'POST'])
@app.route('/b/', methods=['GET', 'POST'])
@app.route('/test/', methods=['GET', 'POST'])
def handle_main():
    # Redirect to include your_id with random number if not present and on root path
    if request.path == '/' and request.method == 'GET' and 'your_id' not in request.args:
        random_id = random.randint(1000, 9999)
        return redirect(url_for('handle_main', your_id=random_id))

    # Get query parameters or form data
    params = request.args if request.method == 'GET' else request.form
    param_count = len(params)
    
    # Check sensitive headers
    headers_response = check_headers()
    if headers_response:
        return headers_response

    # Check parameter count
    if param_count > 30:
        return Response("Too many parameters!", status=400)
    elif param_count > 25:
        return Response("Very high parameter count detected.", status=200)
    elif param_count > 20:
        return Response("High parameter count detected.", status=200)
    elif param_count > 15:
        return Response("Moderate-high parameter count.", status=200)
    elif param_count > 10:
        return Response("Moderate parameter count.", status=200)
    elif param_count > 5:
        return Response("Low-moderate parameter count.", status=200)

    # Process parameters
    response_data = {'message': 'Welcome to the test site!'}
    for param, value in params.items():
        if param == 'your_id':
            response_data[param] = f"Your ID Response: {random.choice(RANDOM_RESPONSES)}"
        elif param in HIDDEN_PARAMS:
            if 'X-Forwarded-For' in request.headers and request.headers['X-Forwarded-For'] == '192.168.1.1':
                response_data[param] = f"Hidden parameter detected with X-Forwarded-For: {param}={HIDDEN_PARAMS[param]}"
            else:
                response_data[param] = f"Hidden parameter detected: {param}={HIDDEN_PARAMS[param]}"
        elif re.match(r'^(home_|a_|secret_|admin_)', param):
            response_data[param] = f"Similar parameter detected: {param}={value}"
        else:
            response_data[param] = f"Standard parameter: {param}={value}"

    # Check for secret_key in POST
    if request.method == 'POST' and 'secret_key' in params:
        return Response("Secret key detected in POST! Possible sensitive action.", status=403)

    # Simulate random server error
    if param_count == 15 and random.random() > 0.7:
        return Response("Internal server error due to parameter processing!", status=500)

    # Generate HTML with form
    html_content = generate_html_form(params)
    return Response(html_content, mimetype='text/html')

def check_headers():
    """Check sensitive headers and return varied responses"""
    for header, values in SENSITIVE_HEADERS.items():
        if header in request.headers and request.headers[header] in values:
            if int(time.time()) % 2 == 0:
                return Response(
                    f"Sensitive header detected: {header}={request.headers[header]} (time-based response)",
                    status=403 if random.random() > 0.5 else 200
                )
            return Response(
                f"Sensitive header detected: {header}={request.headers[header]}",
                status=403 if random.random() > 0.5 else 200
            )
    return None

def generate_html_form(params):
    """Generate a stylish HTML form with hidden parameters"""
    form_fields = ''.join([f'<input type="text" name="{param}" value="test" class="form-input" placeholder="Enter {param}"><br>' 
                           for param in ['s', 'home_samx', 'a_a', 'secret_key', 'admin_token', 'your_id']])
    js_vars = json.dumps({
        'config': {
            'home_same': 'value_e',
            'user_id': '12345',
            'api_key': 'hidden_123',
            'secret_param': 'hidden_456'
        }
    })
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Fuzzing Site</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body {{
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #6e8efb, #a777e3);
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .container {{
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                max-width: 600px;
                width: 90%;
                text-align: center;
                animation: fadeIn 1s ease-in;
            }}
            h1 {{
                color: #2c3e50;
                font-size: 2rem;
                margin-bottom: 1rem;
            }}
            .form-input {{
                width: 100%;
                padding: 0.8rem;
                margin: 0.5rem 0;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 1rem;
                transition: border-color 0.3s;
            }}
            .form-input:focus {{
                border-color: #6e8efb;
                outline: none;
            }}
            .submit-btn {{
                background: #6e8efb;
                color: white;
                padding: 0.8rem 1.5rem;
                border: none;
                border-radius: 5px;
                font-size: 1rem;
                cursor: pointer;
                transition: background 0.3s, transform 0.2s;
            }}
            .submit-btn:hover {{
                background: #a777e3;
                transform: scale(1.05);
            }}
            .params-section {{
                margin-top: 2rem;
                text-align: left;
                background: #f9f9f9;
                padding: 1rem;
                border-radius: 10px;
            }}
            .params-section h2 {{
                font-size: 1.5rem;
                color: #2c3e50;
                margin-bottom: 1rem;
            }}
            .logo {{
                font-size: 1.2rem;
                color: #6e8efb;
                margin-bottom: 1rem;
            }}
            .logo i {{
                margin-right: 0.5rem;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(-20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @media (max-width: 500px) {{
                .container {{
                    padding: 1rem;
                    width: 95%;
                }}
                h1 {{
                    font-size: 1.5rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo"><i class="fas fa-shield-alt"></i>Test Fuzzing Site</div>
            <h1>Welcome to the Fuzzing Test Platform</h1>
            <form method="POST" action="/">
                {form_fields}
                <button type="submit" class="submit-btn">Submit <i class="fas fa-arrow-right"></i></button>
            </form>
            <div class="params-section">
                <h2>Query Parameters</h2>
                <p>{json.dumps(dict(params), indent=2)}</p>
            </div>
        </div>
        <script>
            var hiddenConfig = {js_vars};
            var secretVar = "secret_key";
            var extraVar = "admin_token";
        </script>
    </body>
    </html>
    """
    return html

@app.route('/api', methods=['GET', 'POST'])
def api_endpoint():
    """API endpoint for testing JSON"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            if 'secret_key' in data or 'admin_token' in data:
                return jsonify({'error': 'Sensitive key not allowed in JSON!'}), 403
            return jsonify({'received': data, 'status': 'success'})
        except:
            return jsonify({'error': 'Invalid JSON'}), 400
    return jsonify({'message': 'Send POST with JSON data'})

@app.route('/static/', methods=['GET'])
def static_route():
    """Static route serving simple content"""
    return Response("""
    <html>
        <body>
            <h1>Static Content Page</h1>
            <p>This is a static route for testing purposes.</p>
            <p>Hidden info: static_secret=xyz789</p>
        </body>
    </html>
    """, mimetype='text/html')

@app.route('/static/script.js')
def serve_js():
    """Simulate a JavaScript file with hidden parameters"""
    js_content = """
    var config = {
        secret_param: 'hidden_456',
        another_param: 'value_789',
        api_token: 'token_123'
    };
    """
    return Response(js_content, mimetype='application/javascript')

@app.route('/notfound')
def not_found():
    """Simulate a 404 response with sensitive information leak"""
    return Response("Page not found! Secret: hidden_123", status=404)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)