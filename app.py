from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_item(item_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

def update_quantity(item_id, new_qty):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET quantity = ? WHERE id = ?", (new_qty, item_id))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    item = None
    message = ""
    if request.method == "POST":
        action = request.form.get("action")
        item_id = request.form.get("item_id").strip().upper()
        item = get_item(item_id)

        if not item:
            message = "Item not found."
        else:
            if action == "search":
                pass  # just show item
            elif action == "sell":
                update_quantity(item_id, 0)
                item = get_item(item_id)
                message = "Marked as Sold Out."
            elif action == "add":
                add_qty = int(request.form.get("add_qty", 0))
                update_quantity(item_id, item[2] + add_qty)
                item = get_item(item_id)
                message = f"Added {add_qty} pieces."

    return render_template("index.html", item=item, message=message)

if __name__ == "__main__":
    app.run(debug=True)


