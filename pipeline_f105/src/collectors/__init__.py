"""
Registro central dos coletores. O pipeline itera sobre COLETORES em vez de
importar cada loja manualmente — para adicionar uma loja nova, basta criar
o módulo e registrar aqui.
"""

from . import magazine_luiza, kabum, samsung, casas_bahia, amazon, compra_rapida

COLETORES = {
    "magazine_luiza": magazine_luiza,
    "kabum": kabum,
    "samsung": samsung,
    "casas_bahia": casas_bahia,
    "amazon": amazon,
    "compra_rapida": compra_rapida,
}
