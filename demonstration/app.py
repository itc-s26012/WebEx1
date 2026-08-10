from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'mini_sns_game'

# シナリオデータ（選択肢は2〜4個）
SCENARIO = {
    0: {
        "text": "【拡散希望】今、あなたの街の空に『赤い目』が浮いているのが見えませんか？見つけても絶対に目を合わせないで。",
        "choices": [
            {"text": "窓の外を確認する", "next": 1},
            {"text": "カーテンを閉めて無視する", "next": 2}
        ]  # 選択肢2つ
    },
    1: {
        "text": "＠ユーザー名 見ちゃいましたね。今、目が合いました。あなたの部屋に向かいます。",
        "choices": [
            {"text": "玄関の鍵を閉める", "next": 3},
            {"text": "明かりをすべて消す", "next": 3},
            {"text": "警察に通報する", "next": 4}
        ]  # 選択肢3つ
    },
    2: {
        "text": "賢明な判断です。しかし、タイムラインをよく見てください。トレンドワードがすべて『あなたの本名』になっていますよ。",
        "choices": [
            {"text": "スマホの電源を切る", "next": 4},
            {"text": "自分の名前で検索してみる", "next": 1},
            {"text": "アカウントを削除する", "next": 3},
            {"text": "デマだと信じて寝る", "next": 4}
        ]  # 選択肢4つ
    },
    3: {
        "text": "ガタガタガタ……。窓を激しく叩く音が響く。手遅れだったようだ。【Game Over】",
        "image": "images/kowame.jpeg",
        "choices": [
            {"text": "最初からやり直す", "next": 0}
        ]
    },
    4: {
        "text": "一晩明けると、外は何事もなかったかのように静かだった。あなたは生き延びた……？【Clear】",
        "choices": [
            {"text": "タイトルに戻る", "next": 0}
        ]
    }
}

@app.route('/', methods=['GET', 'POST'])
def game():
    # 初回アクセス時またはリセット時
    if 'stage' not in session or request.method == 'GET':
        session['stage'] = 0

    # 選択肢が送信された場合のステージ更新
    if request.method == 'POST':
        next_stage = request.form.get('next_stage', 0)
        session['stage'] = int(next_stage)

    # 現在のステージデータを取得（存在しない場合は0に戻す）
    current_data = SCENARIO.get(session['stage'], SCENARIO[0])
    return render_template('index.html', data=current_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
