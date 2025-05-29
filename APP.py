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
    """Generate a stylish HTML form with hidden parameters, Your ID link, and My Profile link"""
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
    
    # Generate random ID for the Your ID and My Profile links
    random_id = random.randint(1000, 9999)
    
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
            .your-id-link, .profile-link {{
                display: inline-block;
                margin: 0.5rem 1rem;
                color: #6e8efb;
                text-decoration: none;
                font-size: 1rem;
                transition: color 0.3s;
            }}
            .your-id-link:hover, .profile-link:hover {{
                color: #a777e3;
                text-decoration: underline;
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
            <a href="/?your_id={random_id}" class="your-id-link">Your ID</a>
            <a href="/my_profile/user={random_id}" class="profile-link">My Profile</a>
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
    """Simulate a JavaScript file with hidden parameters and admin endpoint reference"""
    js_content = """
    var config = {
        secret_param: 'hidden_456',
        another_param: 'value_789',
        api_token: 'token_123',
        admin_endpoint: '/my_admin/'
    };
    """
    return Response(js_content, mimetype='application/javascript')

@app.route('/notfound')
def not_found():
    """Simulate a 404 response with sensitive information leak"""
    return Response("Page not found! Secret: hidden_123", status=404)

@app.route('/my_profile/user=<user_id>', methods=['GET', 'POST'])
def my_profile(user_id):
    """User profile page with basic profile information and hackable feature"""
    # Validate user_id
    if not user_id.isalnum():
        return Response("Invalid user ID!", status=400)

    # Check sensitive headers
    headers_response = check_headers()
    if headers_response:
        return headers_response

    # Hackable feature: Hidden admin access via POST with specific parameter
    if request.method == 'POST':
        params = request.form
        if 'access_code' in params and params['access_code'] == 'hackme_1337':
            return Response(
                f"Secret admin access granted! Hidden endpoint: /my_admin/admin=133",
                status=200
            )

    # Generate HTML for the profile page
    html_content = generate_profile_html(user_id)
    return Response(html_content, mimetype='text/html')

def generate_profile_html(user_id):
    """Generate HTML for the user profile page"""
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Profile</title>
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
            .profile-info {{
                background: #f9f9f9;
                padding: 1rem;
                border-radius: 10px;
                margin-top: 1rem;
            }}
            .profile-info p {{
                margin: 0.5rem 0;
                font-size: 1rem;
            }}
            .back-link {{
                display: inline-block;
                margin-top: 1rem;
                color: #6e8efb;
                text-decoration: none;
                font-size: 1rem;
                transition: color 0.3s;
            }}
            .back-link:hover {{
                color: #a777e3;
                text-decoration: underline;
            }}
            .logo {{
                font-size: 1.2rem;
                color: #6e8efb;
                margin-bottom: 1rem;
            }}
            .logo i {{
                margin-right: 0.5rem;
            }}
            .hack-form {{
                margin-top: 1.5rem;
            }}
            .form-input {{
                width: 100%;
                padding: 0.8rem;
                margin: 0.5rem 0;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 1rem;
            }}
            .submit-btn {{
                background: #6e8efb;
                color: white;
                padding: 0.8rem 1.5rem;
                border: none;
                border-radius: 5px;
                font-size: 1rem;
                cursor: pointer;
            }}
            .submit-btn:hover {{
                background: #a777e3;
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
            <div class="logo"><i class="fas fa-user-circle"></i>User Profile</div>
            <h1>Welcome, User {user_id}</h1>
            <div class="profile-info">
                <p><strong>User ID:</strong> {user_id}</p>
                <p><strong>Username:</strong> user_{user_id}</p>
                <p><strong>Email:</strong> user_{user_id}@example.com</p>
                <p><strong>Join Date:</strong> {time.strftime('%Y-%m-%d')}</p>
                <p><strong>Status:</strong> Active</p>
            </div>
            <div class="hack-form">
                <form method="POST" action="/my_profile/user={user_id}">
                    <input type="text" name="access_code" class="form-input" placeholder="Enter access code">
                    <button type="submit" class="submit-btn">Submit Code</button>
                </form>
            </div>
            <a href="/" class="back-link">Back to Home</a>
        </div>
        <script>
            var profileConfig = {{
                user_id: "{user_id}",
                hidden_param: "profile_secret_{random.randint(1000, 9999)}",
                hint: "Try access_code=hackme_1337"
            }};
        </script>
    </body>
    </html>
    """
    return html

@app.route('/my_admin/admin=133', methods=['POST'])
def my_admin():
    """Hidden admin route accessible only with admin=133 via POST"""
    # Check if the exact admin parameter is provided
    if request.path != '/my_admin/admin=1':
        return Response("Invalid admin ID!", status=403)

    # Check sensitive headers
    headers_response = check_headers()
    if headers_response:
        return headers_response

    # Require Authorization header
    if 'Authorization' not in request.headers or request.headers['Authorization'] != 'Bearer secret_token':
        return Response("username = admin , password = arlio_sextu21", status=404)

    # Generate HTML for the admin panel
    html_content = generate_admin_html()
    return Response(html_content, mimetype='text/html')

def generate_admin_html():
    """Generate a visually appealing HTML for the admin panel"""
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Panel</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body {{
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
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
                padding: 2.5rem;
                border-radius: 20px;
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
                max-width: 700px;
                width: 95%;
                text-align: center;
                animation: slideIn 0.8s ease-out;
            }}
            h1 {{
                color: #1e3c72;
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }}
            .subtitle {{
                color: #555;
                font-size: 1.2rem;
                margin-bottom: 2rem;
            }}
            .admin-info {{
                background: linear-gradient(135deg, #e3f2fd, #bbdefb);
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1.5rem 0;
                box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            .admin-info p {{
                margin: 0.8rem 0;
                font-size: 1.1rem;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .admin-info i {{
                margin-right: 0.8rem;
                color: #1e3c72;
            }}
            .action-buttons {{
                margin-top: 2rem;
            }}
            .action-btn {{
                background: #1e3c72;
                color: white;
                padding: 0.8rem 1.5rem;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                margin: 0 0.5rem;
                transition: background 0.3s, transform 0.2s;
            }}
            .action-btn:hover {{
                background: #2a5298;
                transform: translateY(-2px);
            }}
            .back-link {{
                display: inline-block;
                margin-top: 1.5rem;
                color: #1e3c72;
                text-decoration: none;
                font-size: 1rem;
                font-weight: 600;
                transition: color 0.3s;
            }}
            .back-link:hover {{
                color: #2a5298;
                text-decoration: underline;
            }}
            .logo {{
                font-size: 1.5rem;
                color: #1e3c72;
                margin-bottom: 1rem;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .logo i {{
                margin-right: 0.5rem;
                font-size: 1.8rem;
            }}
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateY(-30px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            @media (max-width: 500px) {{
                .container {{
                    padding: 1.5rem;
                    width: 90%;
                }}
                h1 {{
                    font-size: 2rem;
                }}
                .subtitle {{
                    font-size: 1rem;
                }}
                .action-btn {{
                    padding: 0.6rem 1rem;
                    font-size: 0.9rem;
                    margin: 0.3rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo"><i class="fas fa-user-shield"></i>Admin Control Panel</div>
            <h1>Admin Dashboard</h1>
            <p class="subtitle">Manage system settings and configurations</p>
            <div class="admin-info">
                <p><i class="fas fa-id-badge"></i><strong>Admin ID:</strong> 133</p>
                <p><i class="fas fa-shield-alt"></i><strong>Access Level:</strong> Super Administrator</p>
                <p><i class="fas fa-key"></i><strong>Secret Token:</strong> admin_secret_133</p>
                <p><i class="fas fa-clock"></i><strong>Last Login:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><i class="fas fa-cog"></i><strong>Hidden Config:</strong> admin_config_{random.randint(1000, 9999)}</p>
            </div>
            <div class="action-buttons">
                <button class="action-btn" onclick="alert('Manage Users functionality coming soon!')">
                    <i class="fas fa-users"></i> Manage Users
                </button>
                <button class="action-btn" onclick="alert('System Settings functionality coming soon!')">
                    <i class="fas fa-cogs"></i> System Settings
                </button>
            </div>
            <a href="/" class="back-link">Back to Home</a>
        </div>
        <script>
            var adminConfig = {{
                admin_id: "133",
                hidden_param: "admin_secret_{random.randint(1000, 9999)}",
                api_key: "hidden_admin_key_{random.randint(1000, 9999)}"
            }};
        </script>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
