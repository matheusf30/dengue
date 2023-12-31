############################################################################
####### scrpit Matheus analise de acumulados de chuva ######################
####### modelo MERGE                                  ####################### 
#############################################################################

##### faz mapa de acumulado mensal#############################################
'reinit'
'sdfopen MERGE_CPTEC_MONTHLY_2000_2020.nc'
'set lat -29.3 -25.7'
'set lon -54 -48'
'set mpdset hires brmap'
'set grads off'
'set gxout shaded'
'set t 1'
'd prec'
'run cbarn.gs'
'draw title Acumulado Mensal de Chuva \ Junho 2000'
'draw xlab MERGE'
'printim acum_chuva_jun_00.png white'
'c'
##########################################################################
'reinit'
'sdfopen MERGE_CPTEC_MONTHLY_2000_2020.nc'
'set lat -29.3 -25.7'
'set lon -54 -48'
'set mpdset hires brmap'
'set grads off'
'set gxout shaded'
'set t 2'
'd prec'
'run cbarn.gs'
'draw title Acumulado Mensal de Chuva \ Julho 2000'
'draw xlab MERGE'
'printim acum_chuva_jul_00.png white'
'c'
##########################################################################
'reinit'
'sdfopen MERGE_CPTEC_MONTHLY_2000_2020.nc'
'set lat -29.3 -25.7'
'set lon -54 -48'
'set mpdset hires brmap'
'set grads off'
'set gxout shaded'
'set t 3'
'd prec'
'run cbarn.gs'
'draw title Acumulado Mensal de Chuva \ Agosto 2000'
'draw xlab MERGE'
'printim acum_chuva_ago_00.png white'
'c'
##########################################################################
'reinit'
'sdfopen MERGE_CPTEC_MONTHLY_2000_2020.nc'
'set lat -29.3 -25.7'
'set lon -54 -48'
'set mpdset hires brmap'
'set grads off'
'set gxout shaded'
'set t 4'
'd prec'
'run cbarn.gs'
'draw title Acumulado Mensal de Chuva \ Setembro 2000'
'draw xlab MERGE'
'printim acum_chuva_set_00.png white'
'c'
###############################################################################
############## faz serie temporal##########################################
'reinit'
'sdfopen MERGE_CPTEC_MONTHLY_2000_2020.nc'
'set lat -27'
'set lon -48'
'set t 1 13'
'set grads off'
'd prec'scrip_matheus_seu_lindo.gs
'draw title Acumulado de Chuva \ Junho 2000 - Junho 2001'
'printim serie_temp_jun_00_01.png white'
'c'
################################################################################
'reinit'
'sdfopen MERGE_CPTEC_MONTHLY_2000_2020.nc'
'set lat -27'
'set lon -48'
'set t 13 25'
'set grads off'
'd prec'
'draw title Acumulado de Chuva \ Junho 2001 - Junho 2002'
'printim serie_temp_jun_01_02.png white'
'c'
##########################
'reinit'
'sdfopen MERGE_CPTEC_MONTHLY_2000_2020.nc'
'set lat -27'
'set lon -48'
'set t 1 247'
'set grads off'
'd prec'
'draw title Acumulado de Chuva \ Junho 2000 - Junho 2020'
'printim serie_temp_jun_00_20.png white'
'c'
################################
'reinit'
'sdfopen MERGE_CPTEC_MONTHLY_2000_2020.nc'
'set lat -29.3 -25.7'
'set lon -54 -48'
'set t 13'
'set mpdset hires brmap'
'set gxout shaded'
'set grads off'
'd prec'
'run cbarn.gs'
'draw title Acumulado mensal de Chuva \ 2001'
'draw xlab MERGE'
'printim serie_acumulado_jun_01.png white'
'c'
######
'quit'
