from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Hello World")


@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    return """
    <!DOCTYPE html>
    <html>
        <head><title>Hello World</title></head>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>
    """
