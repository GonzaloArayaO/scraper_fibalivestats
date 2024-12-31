import pandas as pd
import numpy as np
from .box_score import box_score

def player_adv_stats(match_id, fecha, fase=None, competencia=None, export_csv=False):
    '''
    Función para extrear data estadisticas avanzadas a nivel jugador de un partido especifico
        -Parametros:
            match_id = id extraido de url original (str)
            fecha = Fecha de dia de partido (DD-MM-AA)
            fase = Fase de campeonato o liga (Regular, playoffs, fases, etc)(str)
            competencia = Nombre competencia
            export_csv = True = exporta a csv (boolean)
    '''
    # Utilización de funcion box_score para generar df
    df = box_score(match_id=match_id, fecha=fecha)

    df_local = df[df['localia'] == 'Local'].reset_index()
    df_visita = df[df['localia'] == 'Visita'].reset_index()

    # Nombre equipos
    local = df_local['equipo'][0]
    visita = df_visita['equipo'][0]

    # Posession
    df_local['poss'] = round(df_local['tci'] + (df_local['tli'] * 0.44) - df_local['ro'] + df_local['per'], 2)
    df_visita['poss'] = round(df_visita['tci'] + (df_visita['tli'] * 0.44) - df_visita['ro'] + df_visita['per'], 2)

    # Plays
    df_local['plays'] = round(df_local['tci'] + (df_local['tli'] * 0.44) + df_local['per'], 2)
    df_visita['plays'] = round(df_visita['tci'] + (df_visita['tli'] * 0.44) + df_visita['per'], 2)

    # USG%
    # Definir usg% en 0 para filtrar jugadores sobre 1 min
    df_local.loc[df_local['min'] > 0.9 , 'usg%'] = round(
        (((df_local['tci'] + df_local['per'] + (df_local['tli'] * 0.44)) * 200) /
        ((df_local['tci'].sum() + df_local['per'].sum() + (df_local['tli'].sum() * 0.44)) * 5 * df_local['min']) * 100) , 2)
    
    df_visita.loc[df_visita['min'] > 0.9 , 'usg%'] = round(
        (((df_visita['tci'] + df_visita['per'] + (df_visita['tli'] * 0.44)) * 200) /
        ((df_visita['tci'].sum() + df_visita['per'].sum() + (df_visita['tli'].sum() * 0.44)) * 5 * df_visita['min']) * 100) , 2)

    # Puntos por tiro
    df_local['pts_t1'] = round((df_local['tlc']) / df_local['tli'], 2)
    df_local['pts_t2'] = round((df_local['t2c'] * 2) / df_local['t2i'], 2)
    df_local['pts_t3'] = round((df_local['t3c'] * 3) / df_local['t3i'], 2)
    df_visita['pts_t1'] = round((df_visita['tlc']) / df_visita['tli'], 2)
    df_visita['pts_t2'] = round((df_visita['t2c'] * 2) / df_visita['t2i'], 2)
    df_visita['pts_t3'] = round((df_visita['t3c'] * 3) / df_visita['t3i'], 2)


    # Porcentaje de distribucion
    df_local['t2i%'] = round(df_local['t2i'] / df_local['t2i'].sum() * 100, 2)
    df_local['t3i%'] = round(df_local['t3i'] / df_local['t3i'].sum() * 100, 2)
    df_local['tci%'] = round(df_local['tci'] / df_local['tci'].sum() * 100, 2)
    df_local['poss_i%'] = round(df_local['poss'] / df_local['poss'].sum() * 100, 2)
    df_local['plays_i%'] = round(df_local['plays'] / df_local['plays'].sum() * 100, 2)
    df_visita['t2i%'] = round(df_visita['t2i'] / df_visita['t2i'].sum() * 100, 2)
    df_visita['t3i%'] = round(df_visita['t3i'] / df_visita['t3i'].sum() * 100, 2)
    df_visita['tci%'] = round(df_visita['tci'] / df_visita['tci'].sum() * 100, 2)
    df_visita['poss_i%'] = round(df_visita['poss'] / df_visita['poss'].sum() * 100, 2)
    df_visita['plays_i%'] = round(df_visita['plays'] / df_visita['plays'].sum() * 100, 2)

    # Distribucion de puntos
    df_local['pts_min'] = round(df_local['pts'] / df_local['min'], 2)
    df_local['pts_tiro'] = round((df_local['t2c'] * 2 + df_local['t3c'] * 3) / (df_local['t2i'] + df_local['t3i']), 2)
    df_local['pts_poss'] = np.where(df_local['poss'] == 0, np.nan, df_local['pts'] / df_local['poss']).round(2)
    df_local['pts_plays'] = np.where(df_local['plays'] == 0, np.nan, df_local['pts'] / df_local['plays']).round(2)
    df_visita['pts_min'] = round(df_visita['pts'] / df_visita['min'], 2)
    df_visita['pts_tiro'] = round((df_visita['t2c'] * 2 + df_visita['t3c'] * 3) / (df_visita['t2i'] + df_visita['t3i']), 2)
    df_visita['pts_poss'] = np.where(df_visita['poss'] == 0, np.nan, df_visita['pts'] / df_visita['poss']).round(2)
    df_visita['pts_plays'] = np.where(df_visita['plays'] == 0, np.nan, df_visita['pts'] / df_visita['plays']).round(2)

    df_local = df_local[[
        'match_id','fecha','#','jugador','equipo','fase','competencia','localia',
        'min','pts','poss','plays','usg%','pts_t1','pts_t2','pts_t3','t2i%','t3i%','tci%','poss_i%',
        'plays_i%','pts_min','pts_tiro','pts_poss','pts_plays'
        ]].sort_values(['localia'], ascending=True)

    df_visita = df_visita[[
        'match_id','fecha','#','jugador','equipo','fase','competencia','localia',
        'min','pts','poss','plays','usg%','pts_t1','pts_t2','pts_t3','t2i%','t3i%','tci%','poss_i%',
        'plays_i%','pts_min','pts_tiro','pts_poss','pts_plays'
        ]].sort_values(['localia'], ascending=True)

    df = pd.concat([df_local, df_visita])
    df = df.fillna(0)
    df['fase'] = fase
    df['competencia'] = competencia

    if export_csv==True:
        df.to_csv(f'../data/player_adv_stats/{local} vs {visita} player_adv_stats - {fecha}.csv', 
        index=False)
        return df
    else:
        return df