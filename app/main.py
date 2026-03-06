from fastapi import FastAPI

app = FastAPI(
    title="IOL Investment Platform",
    version="0.1.0",
    description="Backend API for investment automation and portfolio analysis.",
)


@app.get("/")
def root():
    return {"message": "IOL Investment Platform API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
