import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Change to the summaries directory (one level up from python directory)
os.chdir(Path(__file__).parent.parent / 'summaries')

# Configure the server
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

# Create the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving documentation at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")

    # Open the browser automatically
    webbrowser.open(f'http://localhost:{PORT}')

    # Start serving
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()
