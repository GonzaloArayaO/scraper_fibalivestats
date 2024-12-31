import pandas as pd
from .fiba_response import fiba_response

def box_score(match_id, fecha, fase=None, competencia=None, export_csv=False):

    '''
    Función para extraer data de Box Score de un partido especifico
        -Parametros:
            match_id = id extraido de url original (str)
            fecha = Fecha de dia de partido (DD-MM-AA)
            fase = Fase de campeonato o liga (Regular, playoffs, fases, etc)(str)
            competencia = Nombre competencia
            export_csv = True = exporta a csv (boolean)
    '''

    response = fiba_response(match_id=match_id)
    
    # Creacion de Dfs para equipo local y visitante
    df_local = pd.DataFrame(response['tm']['1']['pl'])
    df_local = df_local.transpose()
    df_visita = pd.DataFrame(response['tm']['2']['pl'])
    df_visita = df_visita.transpose()

    # Añadir nombre equipos y localia
    local = response['tm']['1']['name']
    visita = response['tm']['2']['name']
    df_local['equipo'] = local
    df_visita['equipo'] = visita
    df_local['localia'] = 'Local'
    df_visita['localia'] = 'Visita'

    # Concatecion para geneara box score del partido
    box_score = pd.concat([df_local, df_visita], ignore_index=True)

    # Añadir columnas de parametros
    box_score['fecha'] = fecha
    box_score['fase'] = fase
    box_score['competencia'] = competencia
    box_score['match_id'] = match_id

    # Renombrar columnas 
    box_score.rename(columns={
        'shirtNumber':'#',
        'name':'jugador',
        'firstName':'nombre',
        'familyName':'apellidos',
        'playingPosition':'posicion',
        'starter':'titular',
        'sMinutes':'min',
        'sPoints':'pts',
        'sFieldGoalsMade':'tcc',
        'sFieldGoalsAttempted':'tci',
        'sTwoPointersMade':'t2c',
        'sTwoPointersAttempted':'t2i',
        'sThreePointersMade':'t3c',
        'sThreePointersAttempted':'t3i',
        'sFreeThrowsMade':'tlc',
        'sFreeThrowsAttempted':'tli',
        'sReboundsOffensive':'ro',
        'sReboundsDefensive':'rd',
        'sReboundsTotal':'rt',
        'sAssists':'ast',
        'sTurnovers':'per',
        'sSteals':'rob',
        'sBlocks':'blq',
        'sBlocksReceived':'blq_re',
        'sFoulsPersonal':'fp',
        'sFoulsOn':'fp_re',
        'sPlusMinusPoints':'+/-',
        'eff_1':'val'
        }, inplace=True)

    # Tratar columna min
    box_score['tiempo_de_juego'] = box_score['min'] # Se guarda sin tratar para viz
    box_score[['minutos','segundos']] = box_score['min'].str.split(':', expand=True)

    # Cambiar tipo de datos de columnas a Integer
    columnas_numericas = [
        'pts','tcc','tci','t2c','t2i','t3c','t3i','tlc','tli','ro',
        'rd','rt','ast','per','rob','blq','blq_re','fp','fp_re','+/-',
        'val','minutos','segundos'
        ]
    box_score[columnas_numericas] = box_score[columnas_numericas].apply(pd.to_numeric)

    # Calculo de porcentajes de lanzamiento
    box_score['tc%'] = round(box_score['tcc'] / box_score['tci'], 2)
    box_score['t2%'] = round(box_score['t2c'] / box_score['t2i'], 2)
    box_score['t3%'] = round(box_score['t3c'] / box_score['t3i'], 2)
    box_score['tl%'] = round(box_score['tlc'] / box_score['tli'], 2)

    # Rellenar NaN (divisiones por cero)
    box_score = box_score.fillna(0)

    # Escalar columna min
    box_score['min'] = round(box_score['minutos'] + box_score['segundos'] / 60, 2)

    # Filtracion y orden de Df final
    columnas = [
        'match_id','fecha','#','jugador','nombre','apellidos',
        'equipo','localia','fase','competencia','titular','tiempo_de_juego','min',
        'pts','tcc','tci','tc%','t2c','t2i','t2%','t3c','t3i','t3%','tlc','tli',
        'tl%','ro','rd','rt','ast','per','rob','blq','blq_re','fp','fp_re','+/-','val'
        ]
    box_score = box_score[columnas]

    # Ordenar df por equipo (local y visita) y titularidad
    box_score.sort_values(['localia', 'titular'], ascending=[True, False], inplace=True)


    if export_csv==True:
        box_score.to_csv(
            f'../data/box_score/{local} vs {visita} - {fecha}.csv', index=False
            )
        return box_score
    else:
        return box_score