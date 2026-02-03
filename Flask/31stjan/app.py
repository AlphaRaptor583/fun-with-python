from flask import Flask, render_template, url_for, request, redirect, flash, session, send_from_directory, jsonify, make_response, Response, Blueprint, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.errorhandler(404)
def page_not_found(e):
    
    return "This page does not exist. Please check the URL.", 404

@app.errorhandler(500)
def internal_server_error(e):
    
    return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)
    print(__name__)