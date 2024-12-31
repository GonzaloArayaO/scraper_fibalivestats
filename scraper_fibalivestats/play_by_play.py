import pandas as pd
import numpy as np
from datetime import timedelta
from .fiba_response import fiba_response

def play_by_play(match_id, fecha, fase=None, competencia=None, export_csv=False):

    '''
    Función para extrear data de Play-By-Play de un partido especifico
        -Parametros:
            match_id = id extraido de url original (str)
            fecha = Fecha de dia de partido (DD-MM-AA)
            fase = Fase de campeonato o liga (Regular, playoffs, fases, etc)(str)
            competencia = Nombre competencia
            export_csv = True = exporta a csv (boolean)
    '''

    response = fiba_response(match_id=match_id)
    
    # Creacion de Df con data de Play by play
    pbp = pd.DataFrame(response['pbp']).sort_values('actionNumber')

    # Renombrar columnas
    pbp.rename(columns={
        'gt': 'tiempo_restante',
        's1': 'pts_local',
        's2': 'pts_visita',
        'lead': 'diferencia_pts',
        'period': 'periodo',
        'periodType': 'tipo_periodo',
        'player': 'jugador',
        'firstName':'nombre',
        'familyName':'apellidos',
        'success': 'resultado_evento',
        'actionType': 'evento',
        'actionNumber': 'numero_evento',
        'previousAction': 'evento_previo',
        'qualifier': 'descripcion',
        'subType': 'tipo_evento',
        'shirtNumber': '#'
    }, inplace=True)

    # Cambiar tipo de datos de columnas a Integer
    columnas_numericas = [
            'pts_local', 'pts_visita'
            ]
    pbp[columnas_numericas] = pbp[columnas_numericas].apply(pd.to_numeric)
    
    # Añadir columnas de parametros
    pbp['fecha'] = fecha
    pbp['match_id'] = match_id
    pbp['fase'] = fase
    pbp['competencia'] = competencia

    # Añadir columna equipo 
    pbp['equipo'] = ''
    pbp['equipo'] = np.where(pbp['tno'] == 1, response['tm']['1']['name'], pbp['equipo'])
    pbp['equipo'] = np.where(pbp['tno'] == 2, response['tm']['2']['name'], pbp['equipo'])
    
    # Convertimos la columna 'tiempo' a timedelta
    pbp['tiempo_timedelta'] = pbp['tiempo_restante'].apply(
        lambda x: timedelta(minutes=int(x.split(':')[0]), seconds=int(x.split(':')[1]))
        )
    # Obtener tiempo de juego (REGULAR = 10 min / OVERTIME = 5 min)
    pbp['tiempo_juego'] = pbp.apply(
        lambda row: (timedelta(minutes=10) if row['tipo_periodo'] == 'REGULAR' else timedelta(minutes=5)) - row['tiempo_timedelta'],
        axis=1
        )

    # Convertimos el resultado de nuevo a formato MM:SS
    pbp['tiempo_juego'] = pbp['tiempo_juego'].apply(
        lambda x: f"{int(x.seconds // 60):02}:{int(x.seconds % 60):02}"
        )

    # Eliminamos la columna intermedia 'tiempo_timedelta' si no es necesaria
    pbp.drop(columns=['tiempo_timedelta'], inplace=True)
    # Filtracion y orden de Df final
    pbp = pbp[[
        'match_id','fecha','fase','competencia','tiempo_restante','tiempo_juego','numero_evento',
        '#','jugador','nombre','apellidos','equipo','pts_local','pts_visita',
        'diferencia_pts','periodo','tipo_periodo','evento','resultado_evento',
        'tipo_evento','evento_previo','descripcion' 
    ]]

    local = response['tm']['1']['name']
    visita = response['tm']['2']['name']

    if export_csv==True:
        pbp.to_csv(f'../data/play_by_play/pbp {local} vs {visita} - {fecha}.csv', index=False)
        return pbp
    else:
        return pbp