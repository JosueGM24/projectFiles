from flask import Flask, render_template, request, redirect, url_for
import socket
import requests

app = Flask(__name__)

SERVERS = {
    'debian': ('224.1.1.1', 5007),
    'fedora': ('224.1.1.2', 5007),
    'solaris': ('224.1.1.3', 5007),
    'freebsd': ('224.1.1.4', 5007)
}

selected_server = None

@app.route('/')
def index():
    return render_template('index.html', servers=SERVERS.keys())

@app.route('/select_server', methods=['POST'])
def select_server():
    global selected_server
    selected_server = request.form['server']
    return redirect(url_for('files'))

@app.route('/files')
def files():
    if selected_server is None:
        return redirect(url_for('index'))
    ip, port = SERVERS[selected_server]
    response = requests.get(f'http://{ip}:{port}/files')
    files = response.json().get('files', [])
    return render_template('files.html', files=files, server=selected_server)

@app.route('/upload', methods=['POST'])
def upload():
    if selected_server is None:
        return redirect(url_for('index'))
    file = request.files['file']
    ip, port = SERVERS[selected_server]
    files = {'file': file}
    response = requests.post(f'http://{ip}:{port}/files', files=files)
    return redirect(url_for('files'))

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    if selected_server is None:
        return redirect(url_for('index'))
    ip, port = SERVERS[selected_server]
    response = requests.delete(f'http://{ip}:{port}/files/{filename}')
    return redirect(url_for('files'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
