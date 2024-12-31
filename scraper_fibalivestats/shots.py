import pandas as pd
from .fiba_response import fiba_response
from .play_by_play import play_by_play

def shots(match_id, fecha, fase=None, competencia=None, export_csv=False):
    '''
    Función para extrear data de shots y coordenadas de un partido especifico
        -Parametros:
            match_id = id extraido de url original (str)
            fecha = Fecha de dia de partido (DD-MM-AA)
            fase = Fase de campeonato o liga (Regular, playoffs, fases, etc)(str)
            competencia = Nombre competencia
            export_csv = True = exporta a csv (boolean)
    '''
    # Creacion de Dfs con data de shots
    response = fiba_response(match_id=match_id)
    shots_local = pd.DataFrame(response['tm']['1']['shot'])
    shots_local['club'] = response['tm']['1']['name']
    shots_visita = pd.DataFrame(response['tm']['2']['shot'])
    shots_visita['club'] = response['tm']['2']['name']
    
    # Concatenacion de Dfs y ordenar 
    shots = pd.concat([shots_local, shots_visita], ignore_index=True).sort_values('actionNumber')

    # Renombrar columnas
    shots.rename(columns={
        'r':'resultado',
        'per':'periodo',
        'perType':'tipo_periodo',
        'actionType':'evento',
        'actionNumber':'numero_evento',
        'subType':'tipo_evento',
        'player':'jugador',
        'shirtNumber':'#'
    }, inplace=True)

    # Redondear coordenadas a 2 decimales    
    shots['x'] = round(shots['x'], 2)
    shots['y'] = round(shots['y'], 2)
    
    # Añadir columnas de parametros
    shots['match_id'] = match_id
    shots['fecha'] = fecha
    shots['fase'] = fase
    shots['competencia'] = competencia

    # Añadir columna de minuto y seg
    pbp = play_by_play(
        match_id=match_id,
        fecha=fecha,
        fase=fase,
        competencia=competencia
        )
    pbp = pbp[['tiempo_juego','tiempo_restante','numero_evento']]

    # Merge para añadir columna 'tiempo_partido'
    shots = pd.merge(shots, pbp[['numero_evento','tiempo_restante','tiempo_juego']], on='numero_evento', how='left')

    # Filtracion y orden de Df final
    shots = shots[[
        'match_id','fecha','fase','competencia','numero_evento','#','jugador','club', 
        'evento','resultado','x','y','tipo_evento','periodo','tipo_periodo',
        'tiempo_restante','tiempo_juego'
    ]]
        
    local = response['tm']['1']['name']
    visita = response['tm']['2']['name']

    if export_csv==True:
        shots.to_csv(f'../data/shots/shots {local} vs {visita} - {fecha}.csv', index=False)
        return shots
    else:
        return shots