from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar_db():
    conn = sqlite3.connect('tavinnti.db')
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    conn = conectar_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco TEXT NOT NULL,
            img TEXT,
            pix INTEGER
        )
    ''')
    conn.commit()
    conn.close()

criar_tabela()

@app.route('/')
def index():
    conn = conectar_db()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    return render_template('index.html', lista_produtos=produtos)

@app.route('/admin')
def admin():
    conn = conectar_db()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    return render_template('admin.html', lista_produtos=produtos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    preco = request.form.get('preco')
    img = request.form.get('img')
    pix = 1 if request.form.get('pix') == 'on' else 0
    conn = conectar_db()
    conn.execute('INSERT INTO produtos (nome, descricao, preco, img, pix) VALUES (?, ?, ?, ?, ?)',
                 (nome, descricao, preco, img, pix))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = conectar_db()
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
