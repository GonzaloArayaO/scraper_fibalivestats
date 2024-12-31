import pandas as pd
from .fiba_response import fiba_response

def team_box_score(match_id, fecha, fase=None, competencia=None, export_csv=False):
    '''
    Función para extrear data estadisticas a nivel equipo de un partido especifico
        -Parametros:
            match_id = id extraido de url original (str)
            fecha = Fecha de dia de partido (DD-MM-AA)
            fase = Fase de campeonato o liga (Regular, playoffs, fases, etc)(str)
            competencia = Nombre competencia
            export_csv = True = exporta a csv (boolean)
    '''
    response = fiba_response(match_id=match_id)
    
    # Creacion de Dfs para equipo local y visitante
    df_local = response['tm']['1']
    df_local = pd.DataFrame([df_local])
    df_visita = response['tm']['2']
    df_visita = pd.DataFrame([df_visita])

    # Concatecion para geneara box score del partido
    team_stats = pd.concat([df_local, df_visita], ignore_index=True)

    # Renombrar columnas
    team_stats.rename(columns={
        'name':'equipo',
        'code':'cod_equipo',
        'coach':'dt',
        'score':'pts',
        'tot_sMinutes':'min',
        'tot_sFieldGoalsMade':'tcc',
        'tot_sFieldGoalsAttempted':'tci',
        'tot_sTwoPointersMade':'t2c',
        'tot_sTwoPointersAttempted':'t2i',
        'tot_sThreePointersMade':'t3c',
        'tot_sThreePointersAttempted':'t3i',
        'tot_sFreeThrowsMade':'tlc',
        'tot_sFreeThrowsAttempted':'tli',
        'tot_sReboundsOffensive':'ro',
        'tot_sReboundsDefensive':'rd',
        'tot_sReboundsTotal':'rt',
        'tot_sAssists':'ast',
        'tot_sTurnovers':'per',
        'tot_sSteals':'rob',
        'tot_sBlocks':'blq',
        'tot_sBlocksReceived':'blq_re',
        'tot_sFoulsPersonal':'fp',
        'tot_sFoulsOn':'fp_re',
        'tot_sBenchPoints':'pts_banca',
        'tot_sPointsFastBreak':'pts_contraataque',
        'tot_sPointsFromTurnovers':'pts_por_perdida',
        'tot_sPointsInThePaint':'pts_en_pintura',
        'tot_sPointsSecondChance':'pts_segunda_oportunidad',
        'tot_eff_1':'val'
        }, inplace=True)

    # Tratar columna min
    team_stats[['minutos','segundos']] = team_stats['min'].str.split(':', expand=True)

    # Cambiar tipo de datos de columnas a Integer
    columnas_numericas = [
        'pts','tcc','tci','t2c','t2i','t3c','t3i','tlc','tli','ro',
        'rd','rt','ast','per','rob','blq','blq_re','fp','fp_re','val',
        'pts_banca','pts_contraataque','pts_por_perdida','pts_en_pintura',
        'pts_segunda_oportunidad','minutos','segundos'
        ]
    team_stats[columnas_numericas] = team_stats[columnas_numericas].apply(pd.to_numeric)

    # Añadir columnas de parametros
    team_stats['fecha'] = fecha
    team_stats['fase'] = fase
    team_stats['competencia'] = competencia
    team_stats['match_id'] = match_id

    # Calculo de porcentajes de lanzamiento   
    team_stats['tc%'] = round(team_stats['tcc'] / team_stats['tci'], 2)
    team_stats['t2%'] = round(team_stats['t2c'] / team_stats['t2i'], 2)
    team_stats['t3%'] = round(team_stats['t3c'] / team_stats['t3i'], 2)
    team_stats['tl%'] = round(team_stats['tlc'] / team_stats['tli'], 2)

    # Escalar columna min
    team_stats['min'] = round(team_stats['minutos'] + team_stats['segundos'] / 60, 2)
    team_stats['min'] = team_stats['min'].astype(int)
    team_stats = team_stats.fillna(0)

    # Filtracion y orden de Df final    
    columnas = [
        'match_id','fecha','equipo','cod_equipo','dt','fase','min','pts','tcc',
        'tci','tc%','t2c','t2i','t2%','t3c','t3i','t3%','tlc','tli','tl%',
        'ro','rd','rt','ast','per','rob','blq','blq_re','fp','fp_re','val',
        'pts_banca','pts_contraataque','pts_por_perdida','pts_en_pintura',
        'pts_segunda_oportunidad'
        ]
    team_stats = team_stats[columnas]

    local = response['tm']['1']['name']
    visita = response['tm']['2']['name']

    if export_csv==True:
        team_stats.to_csv(f'../data/team_box_score/{local} vs {visita} totales - {fecha}.csv', index=False)
        return team_stats
    else:
        return team_stats