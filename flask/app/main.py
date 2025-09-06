from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def home():
    img_url = url_for("static", filename="itskiran-color.jpg")
    return f"""
        <html>
          <head>
            <style>
              body {{
                background-color: #2f8da3;
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
              }}
              img {{
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
              }}
              h1 {{
                color: white;
              }}
            </style>
          </head>
          <body>
            <h1>coming soon...</h1>
            <img src="{img_url}" alt="ItsKiran Image" width="400">
          </body>
        </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


# #2f8da3
