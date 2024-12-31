import pathlib
from setuptools import find_packages, setup

# Ruta al directorio actual
HERE = pathlib.Path(__file__).parent

# Metadatos del paquete
VERSION = '0.1.0'
PACKAGE_NAME = 'scraper_fibalivestats'
AUTHOR = 'Gonzalo Araya'
AUTHOR_EMAIL = 'gonzalo.araya24@gmail.com'
URL = 'https://github.com/GonzaloArayaO/scraper_fibalivestats'

LICENSE = 'MIT'
DESCRIPTION = 'Paquete para extraer datos de FIBA Live Stats'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

# Dependencias requeridas
INSTALL_REQUIRES = [
    'pandas',
    'numpy',
    'requests'
]

# Configuración del paquete
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)