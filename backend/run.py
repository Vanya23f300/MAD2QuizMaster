print("run.py is being executed")

from app import create_app

print("Imported create_app")

app = create_app()

print("App created")

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)