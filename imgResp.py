from flask import Flask, request, jsonify
from getImgs import ImgCrawler

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def search():
    keyword = request.form.get('keyword')
    img_crawler = ImgCrawler()
    return jsonify(img_crawler.search(keyword))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
