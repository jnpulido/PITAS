from fastapi import FastAPI
from app.routers.production.router import router as recipes_router
 


 # 😀 😄 😎 🤖 👀 👍 👎 🙌 💡 🎯
 # # ✅ ❌ ⚠️ 🚧 🛠️ 🔄 ⏳ 🚀 🎉 📌

app = FastAPI(title="PITAS")

app.include_router(recipes_router)
