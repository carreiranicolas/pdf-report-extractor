from pathlib import PosixPath
from pydantic.dataclasses import dataclass



@dataclass
class ColunasNumericasModel:
    """Modelo referente ao nome da coluna numerica"""
    nome: str 

@dataclass
class DiretoriosModel:
    """Modelo referente aos caminhos de input e output dos diretorios"""
    input: PosixPath
    output: PosixPath

@dataclass
class ArquivoModel:
    """Modelo referente ao caminho do arquivo final"""
    caminho: PosixPath

@dataclass
class SheetModel:
    """Modelo referente ao nome das sheets no arquivo .xlsx"""
    tabela_itens: str
    valores_finais: str



@dataclass
class ParametrosModel:
    """Modelo referente aos parametros do projeto"""
    colunas_numericas: list[ColunasNumericasModel]
    diretorios: DiretoriosModel 
    arquivo: ArquivoModel
    sheets: SheetModel

