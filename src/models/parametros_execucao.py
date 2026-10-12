from pydantic.dataclasses import dataclass

@dataclass
class ParametrosExecucaoModel:
    """Modelo referente aos parametros de execução passados na .env"""
    remetente: str
    destinatario: str
    app_password: str