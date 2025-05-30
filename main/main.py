from fastapi import FastAPI, HTTPException, APIRouter
import importlib
import pkgutil



app = FastAPI()

def load_api_modules(app, package_name, tags=[]):
    package = __import__(package_name, fromlist=[""])

    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__):
        if is_pkg:
            load_api_modules(app, package_name + "." + module_name, tags)
        else:
            module = importlib.import_module("." + module_name, package_name)
            if hasattr(module, "router"):
                prefix = "/" + "/".join(package_name.split(".")[:-1]) + "/" + module_name
                router = APIRouter()
                router.include_router(module.router, prefix=prefix, tags=tags)
                app.include_router(router)
    return app

@app.get("/health")
async def healthcheck():
    try:
        # Aqui você pode adicionar verificações adicionais, como:
        # - Verificar conexão com o banco de dados
        # - Verificar disponibilidade de serviços externos
        return {"status": "ok"}
    except Exception as e:
        # Se houver algum problema, você pode retornar uma mensagem de erro apropriada
        raise HTTPException(status_code=500, detail=f"Healthcheck failed: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    pass

app = load_api_modules(app, package_name="notebooklm", tags=["notebooklm"])