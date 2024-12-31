import pandas as pd
from .team_box_score import team_box_score

def team_adv_stats(match_id, fecha, fase=None, competencia=None, export_csv=False):
    '''
    Función para extrear data estadisticas avanzadas a nivel equipo de un partido especifico
        -Parametros:
            match_id = id extraido de url original (str)
            fecha = Fecha de dia de partido (DD-MM-AA)
            fase = Fase de campeonato o liga (Regular, playoffs, fases, etc)(str)
            competencia = Nombre competencia
            export_csv = True = exporta a csv (boolean)
    '''
    # Utilización de funcion team_box_score para generar df
    df = team_box_score(match_id=match_id, fecha=fecha)

    local = df['equipo'][0]
    visita = df['equipo'][1]

    # Se hace un df separado de las stats de cada equipo
    df_local = df.iloc[[0]]
    df_visita = df.iloc[[1]]

    # En un df se unen las stats para tener estadisticas de local y visita para cada equipo
    df1 = df_local.merge(df_visita, on='match_id', suffixes=['_local', '_visita'])
    df2 = df_visita.merge(df_local, on='match_id', suffixes=['_local', '_visita'])
    partido_adv = pd.concat([df1, df2], ignore_index=True)

    # Filtrado de columnas necesarias
    partido_adv = partido_adv[[
        'match_id','equipo_local','min_local','pts_local','tcc_local','tci_local', 
        't2c_local','t2i_local','t3c_local','t3i_local','tlc_local','tli_local','ro_local', 
        'rd_local','rt_local','ast_local','per_local','rob_local','blq_local','blq_re_local', 
        'fp_local','fp_re_local','val_local','equipo_visita','pts_visita','tcc_visita','tci_visita', 
        't2c_visita','t2i_visita','t3c_visita','t3i_visita','tlc_visita','tli_visita','ro_visita', 
        'rd_visita','rt_visita','ast_visita','per_visita','rob_visita','blq_visita','blq_re_visita', 
        'fp_visita','fp_re_visita','val_visita'
        ]]

    # Formulas para cada estadistica avanzada por equipo
    partido_adv['poss_local'] = round((partido_adv['tci_local'] + (0.44 * partido_adv['tli_local']) + partido_adv['per_local'] - partido_adv['ro_local']), 2)
    partido_adv['poss_visita'] = round((partido_adv['tci_visita'] + (0.44 * partido_adv['tli_visita']) + partido_adv['per_visita'] - partido_adv['ro_visita']), 2)

    partido_adv['plays_local'] = round((partido_adv['tci_local'] + (0.44 * partido_adv['tli_local']) + partido_adv['per_local']), 2)
    partido_adv['plays_visita'] = round((partido_adv['tci_visita'] + (0.44 * partido_adv['tli_visita']) + partido_adv['per_visita']), 2)

    partido_adv['pace_local'] = round((partido_adv['plays_local'] - partido_adv['ro_local'] + partido_adv['plays_visita'] - partido_adv['ro_visita']) / 2 * 200 / (partido_adv['min_local']), 2)
    partido_adv['pace_visita'] = round((partido_adv['plays_visita'] - partido_adv['ro_visita'] + partido_adv['plays_local'] - partido_adv['ro_local']) / 2 * 200 / (partido_adv['min_local']), 2)

    partido_adv['oer_local'] = round((partido_adv['pts_local'] / partido_adv['plays_local']), 2)
    partido_adv['oer_visita'] = round((partido_adv['pts_visita'] / partido_adv['plays_visita']), 2)

    partido_adv['der_local'] = round((partido_adv['pts_visita'] / partido_adv['plays_visita']), 2)
    partido_adv['der_visita'] = round((partido_adv['pts_local'] / partido_adv['plays_local']), 2)

    partido_adv['net_rtg_local'] = round((partido_adv['oer_local'] - partido_adv['der_local']), 2)
    partido_adv['net_rtg_visita'] = round((partido_adv['oer_visita'] - partido_adv['der_visita']), 2)

    # EFG% 1-FACTOR (40%)
    partido_adv['efg%_local'] = round((((partido_adv['tcc_local'] + 0.5 * partido_adv['t3c_local']) / partido_adv['tci_local']) * 100), 2)
    partido_adv['efg%_visita'] = round((((partido_adv['tcc_visita'] + 0.5 * partido_adv['t3c_visita']) / partido_adv['tci_visita']) * 100), 2)

    partido_adv['ts%_local'] = round((partido_adv['pts_local'] / (2 * (partido_adv['tci_local'] + 0.44 * partido_adv['tli_local'])) * 100), 2)
    partido_adv['ts%_visita'] = round((partido_adv['pts_visita'] / (2 * (partido_adv['tci_visita'] + 0.44 * partido_adv['tli_visita'])) * 100), 2)

    # RO% 3-FACTOR (20%)
    partido_adv['ro%_local'] = round(((partido_adv['ro_local'] / (partido_adv['ro_local'] + partido_adv['rd_visita'])) * 100), 2)
    partido_adv['rd%_local'] = round(((partido_adv['rd_local'] / (partido_adv['ro_visita'] + partido_adv['rd_local'])) * 100), 2)
    partido_adv['tr%_local'] = round(((partido_adv['ro%_local'] + partido_adv['rd%_local']) / 2), 2)

    partido_adv['ro%_visita'] = round(((partido_adv['ro_visita'] / (partido_adv['ro_visita'] + partido_adv['rd_local'])) * 100), 2)
    partido_adv['rd%_visita'] = round(((partido_adv['rd_visita'] / (partido_adv['ro_local'] + partido_adv['rd_visita'])) * 100), 2)
    partido_adv['tr%_visita'] = round(((partido_adv['ro%_visita'] + partido_adv['rd%_visita']) / 2), 2)

    # TO% 2-FACTOR (25%)
    partido_adv['per%_local'] = round(((partido_adv['per_local'] / partido_adv['plays_local']) * 100), 2)
    partido_adv['per%_visita'] = round(((partido_adv['per_visita'] / partido_adv['plays_visita']) * 100), 2)

    # RTL% 4-FACTOR (15%)
    partido_adv['rtl%_local'] = round(((partido_adv['tlc_local'] / partido_adv['tci_local']) * 100), 2)
    partido_adv['rtl%_visita'] = round(((partido_adv['tlc_visita'] / partido_adv['tci_visita']) * 100), 2)

    # Puntos por tiro
    partido_adv['pts_t1_local'] = round((partido_adv['tlc_local']) / partido_adv['tli_local'], 2)
    partido_adv['pts_t1_visita'] = round((partido_adv['tlc_visita']) / partido_adv['tli_visita'], 2)

    partido_adv['pts_t2_local'] = round((partido_adv['t2c_local'] * 2) / partido_adv['t2i_local'], 2)
    partido_adv['pts_t2_visita'] = round((partido_adv['t2c_visita'] * 2) / partido_adv['t2i_visita'], 2)

    partido_adv['pts_t3_local'] = round((partido_adv['t3c_local'] * 3) / partido_adv['t3i_local'], 2)
    partido_adv['pts_t3_visita'] = round((partido_adv['t3c_visita'] * 3) / partido_adv['t3i_visita'], 2)

    # % distribucion tipo de tiro por el total
    partido_adv['t2i%_local'] = round(((partido_adv['t2i_local'] / partido_adv['tci_local']) * 100), 2)   
    partido_adv['t2i%_visita'] = round(((partido_adv['t2i_visita'] / partido_adv['tci_visita']) * 100), 2)

    partido_adv['t3i%_local'] = round(((partido_adv['t3i_local'] / partido_adv['tci_local']) * 100), 2)
    partido_adv['t3i%_visita'] = round(((partido_adv['t3i_visita'] / partido_adv['tci_visita']) * 100), 2)

    # Filtrado de columnas solo con stats avanzadas
    partido_adv = partido_adv[[
        'match_id','equipo_local', 'pts_local','equipo_visita','min_local','pts_visita',
        'poss_local','poss_visita', 'plays_local', 'plays_visita','pace_local', 'pace_visita', 
        'oer_local', 'oer_visita','der_local','der_visita','net_rtg_local', 'net_rtg_visita',
        'efg%_local','efg%_visita', 'ts%_local','ts%_visita','ro%_local','rd%_local','tr%_local',
        'ro%_visita','rd%_visita', 'tr%_visita','per%_local','per%_visita','rtl%_local',
        'rtl%_visita', 'pts_t1_local', 'pts_t1_visita', 'pts_t2_local', 'pts_t2_visita', 'pts_t3_local', 
        'pts_t3_visita', 't2i%_local', 't2i%_visita', 't3i%_local', 't3i%_visita'
        ]]

    partido_adv = partido_adv[partido_adv['equipo_local'] != partido_adv['equipo_visita']]

    partido_adv['fecha'] = fecha
    partido_adv['fase'] = fase
    partido_adv['competencia'] = competencia
    
    partido_adv = partido_adv[[
        'match_id','fecha','fase','competencia','equipo_local','min_local','pts_local','poss_local',
        'plays_local','pace_local','oer_local','der_local','net_rtg_local','efg%_local','ts%_local',
        'ro%_local','rd%_local','tr%_local','per%_local','rtl%_local', 'pts_t1_local', 'pts_t2_local', 
        'pts_t3_local','t2i%_local', 't3i%_local'
        ]]

    # Renombrar columnas a df final
    partido_adv.rename(columns={
        'equipo_local': 'equipo',
        'min_local': 'min',
        'pts_local':'pts',
        'poss_local':'poss',
        'plays_local':'plays',
        'pace_local':'pace',
        'oer_local':'oer',
        'der_local':'der',
        'net_rtg_local':'net_rtg',
        'efg%_local':'efg%',
        'ts%_local':'ts%',
        'ro%_local':'ro%',
        'rd%_local':'rd%',
        'tr%_local':'tr%',
        'per%_local':'per%',
        'rtl%_local':'rtl%',
        'pts_t1_local': 'pts_t1',
        'pts_t2_local': 'pts_t2',
        'pts_t3_local': 'pts_t3',
        '2pi%_local': '2pi%',
        '3pi%_local': '3pi%'
        }, inplace=True)

    if export_csv==True:
        partido_adv.to_csv(f'../data/team_adv_stats/{local} vs {visita} team_adv_stats - {fecha}.csv', 
        index=False)
        return partido_adv
    else:
        return partido_adv