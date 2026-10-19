from fastapi import FastAPI

app= FastAPI(title="Atlas AI")

@app.get("/health")
def health():
    return{"status":"ok"}
@app.get("/name")
def name():
    return{"name":"Atlas AI"}

