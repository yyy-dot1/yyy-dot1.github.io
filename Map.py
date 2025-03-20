from flask import Flask, render_template
import mysql.connector
import folium

app = Flask(__name__)

def create_map():
    # MySQLサーバーに接続
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yuinakba40",
        database="my_db01"
    )
    cursor = conn.cursor()

    # 地図の中心位置を決める（例: 東京）
    map_center = [35.6762, 139.6503]

    # foliumで地図を作成
    my_map = folium.Map(location=map_center, zoom_start=12)

    # データを取得
    cursor.execute("SELECT lat, lon, artifact FROM map_data")
    rows = cursor.fetchall()

    # 出土物ごとの色を定義
    artifact_colors = {
        "dummy": "red",
        "stone": "blue",
        "nife": "orange",
        "bawl": "pink"
    }

    # 取得したデータを地図にプロット
    for row in rows:
        latitude, longitude, artifact = row
        pin_color = artifact_colors.get(artifact, "gray")  # デフォルトは gray
        popup_text = f"出土品: {artifact}" if artifact else "出土品情報なし"

        folium.Marker(
            location=[latitude, longitude],
            popup=popup_text,
            icon=folium.Icon(color=pin_color)
        ).add_to(my_map)

    # HTMLに保存
    map_file = "templates/map.html"
    my_map.save(map_file)

    # 接続を閉じる
    cursor.close()
    conn.close()

    return "map.html"

@app.route("/")
def index():
    map_file = create_map()
    return render_template(map_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
