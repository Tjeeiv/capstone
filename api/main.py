from fastapi import FastAPI

app = FastAPI(
    title="SmartRetail 360 API",
    description="Sales forecasting and review assistant API",
    version="1.0.0"
)

try:
    from api.routes import predict
    app.include_router(predict.router)
    print("✅ predict router registered")
except Exception as e:
    print(f"❌ Failed to register predict router: {e}")

try:
    from api.routes import assistant
    app.include_router(assistant.router)
    print("✅ assistant router registered")
except Exception as e:
    print(f"❌ Failed to register assistant router: {e}")

@app.get("/")
def root():
    return {"status": "SmartRetail 360 API is running"}