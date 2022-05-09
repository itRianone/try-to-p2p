from flask import Flask, redirect, render_template

app = Flask(__name__)


@app.route('/{bill_uid}', methods=['GET'])
def index1(bill_uid):
    print(f'/{bill_uid} now')
    return redirect(
        f"https://vk.com/away.php?to=http://localhost:5000/second/{bill_uid}",
        code=308,
    )
    #return 'Index Page'

@app.route('/second/{bill_uid}', methods=['GET'])
def hello2(bill_uid):
    print(f'/second/{bill_uid} now')
    return redirect(f"https://oplata.qiwi.com/form?invoiceUid={bill_uid}",
    code=308)

@app.route('/bill/{bill_uid}', methods=['GET'])
def hello3(bill_uid):
    print(f'/bill/{bill_uid} now')
    return render_template(f"""<script>
  location.href = "https://oplata.qiwi.com/form?invoiceUid={bill_uid}"
</script>""",
    code=308)

@app.route('/', methods=['GET'])
def hello4():
    print('/ now')
    return 'Hello, World'

app.run()