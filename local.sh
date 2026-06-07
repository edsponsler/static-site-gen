# Runs the static site generator
# Always run this from the project root directory

python src/main.py
cd public && python -m http.server 8888
