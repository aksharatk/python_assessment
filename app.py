from flask import Flask, request, redirect, render_template, flash
import string
import random
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for flash messages

# In-memory storage for URL mappings
url_map = {}

def generate_short_code(url):
    """Generate a 6-character short code using MD5 hash of the URL."""
    hash_object = hashlib.md5(url.encode()).hexdigest()
    return hash_object[:6]

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle the main page with URL shortening form."""
    short_url = None
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        if not long_url:
            flash('Please enter a valid URL.', 'error')
        else:
            # Ensure URL starts with http:// or https://
            if not long_url.startswith(('http://', 'https://')):
                long_url = 'http://' + long_url
            # Check if URL already exists
            for code, url in url_map.items():
                if url == long_url:
                    short_url = request.url_root + code
                    flash('Short URL generated successfully!', 'success')
                    return render_template('index.html', short_url=short_url)
            # Generate new short code
            short_code = generate_short_code(long_url)
            while short_code in url_map:  # Avoid collisions
                short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            url_map[short_code] = long_url
            short_url = request.url_root + short_code
            flash('Short URL generated successfully!', 'success')
    return render_template('index.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirect short code to original URL."""
    long_url = url_map.get(short_code)
    if long_url:
        return redirect(long_url)
    else:
        flash('Invalid or expired short URL.', 'error')
        return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)