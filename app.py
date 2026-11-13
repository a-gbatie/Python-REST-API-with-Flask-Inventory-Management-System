from app import create_app # import create_app() from /app.__init__

app = create_app() # creates Flask app

if __name__ == "__main__": # starts the development server
  app.run(debug=True)