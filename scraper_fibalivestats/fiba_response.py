import requests

def fiba_response(match_id):
    '''
    Conexión con end point de API de FIBA Live Stats
    '''
    headers = headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }

    url = f'https://fibalivestats.dcd.shared.geniussports.com/data/{match_id}/data.json'
    response = requests.get(url, headers=headers).json()
    return response