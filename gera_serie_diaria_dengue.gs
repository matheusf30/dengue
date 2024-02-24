function geral(args)
'reinit'
#
#########################################################################
### Esse script tem como objetivo gerar a Serie temporal dos dados de ###
### temperatura e Produto de Precipitacao SAMET/MERGE. É gerada uma   ###
### tabela para o Estudo da CLeusa/Matheus                            ###
###                                                                   ###
### Elaborado por: Mario Quadro                                       ###                                 ###                                                                   ###
### Para rodar :                                                      ###
###   "run gera_serie_diaria_samet.gs YYYYMM(i) yyyymm(f) ncit"       ###
###                                  Adaptado em:   01/01/2023        ###
#########################################################################
#
#########################################################################
###                  Pegando Parametros de Entrada                    ###
#########################################################################
#
_datai=subwrd(args,1)
_anoi=substr(_datai,1,4)
_mesi=substr(_datai,5,2)
_diai=substr(_datai,7,2)
#_diai=substr(_datai,7,2)
#
_dataf=subwrd(args,2)
_anof=substr(_dataf,1,4)
_mesf=substr(_dataf,5,2)
#_diaf=substr(_dataf,7,2)
#
_nanos=_anof-_anoi+1
#
_ncit=1   
# Pega o valor da Latitude
_lat=subwrd(args,3) 
# Pega o valor da Longitude
_lon=subwrd(args,4)  
# Pega a localidade
_loc=subwrd(args,6) 
# Pega o Código da Estação
_cod=subwrd(args,5)
# Escreve o Cabeçalho ou não da estação
_cab=subwrd(args,7)
#
#
say 'Data Inicial  -> '_anoi%_mesi
say 'Data Final    -> '_anof%_mesf
say 'No de Anos    -> '_nanos
say 'No de Cidades -> '_ncit
#
##########################################
# DEFINE CONSTANTES
##########################################
#
_nmon='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC JAN'
ldy=' 31  28  31  30  31  30  31  31  30  31  30  31'
#
#_fscmer=60*60*24  ;# Fator de Escala para multiplicar na Variavel do MERRA
_fscmer=60*60     ;# Fator de Escala para multiplicar na Variavel do MERRA
_fsccpc=0.1       ;# Fator de Escala para multiplicar na Variavel do CPC
_fscmge=1         ;# Fator de Escala para multiplicar na Variavel do MERGE
_fscchp=1         ;# Fator de Escala para multiplicar na Variavel do CHIRPS
_fsceri=1000      ;# Fator de Escala para multiplicar na Variavel do ERA INTERIM
_fscnc1=60*60*24  ;# Fator de Escala para multiplicar na Variavel do NCEP 1
_fscnc2=60*60*24  ;# Fator de Escala para multiplicar na Variavel do NCEP 2
_fsccfs=60*60*24  ;# Fator de Escala para multiplicar na Variavel do NCEP CFS
_fsce40=1         ;# Fator de Escala para multiplicar na Variavel do ERA 40
#
#########################################################################
###                              Define paths                         ###
#########################################################################
#
#_path_sam='/dados/operacao/samet/daily'        ;# Path SAMET SIFAP
_path_sam='/media/dados/operacao/samet/daily/'  ;# Path SAMET CLUSTER
_path_mge='/media/dados/operacao/merge'               ;# Path MERGE CLUSTER
_path_out='out_data'
#
#########################################################################
###                      Abre Arquivo descritor                       ###
#########################################################################
#
'open '_path_sam'/TMAX/SAMeT_CPTEC_TMAX.ctl'
say _path_sam'/TMAX/SAMeT_CPTEC_TMAX.ctl'
#
'open '_path_sam'/TMED/SAMeT_CPTEC_TMED.ctl'
say _path_sam'/TMED/SAMeT_CPTEC_TMED.ctl'
#
'open '_path_sam'/TMIN/SAMeT_CPTEC_TMIN.ctl'
say _path_sam'/TMIN/SAMeT_CPTEC_TMIN.ctl'
#
'open '_path_mge'/MERGE_CPTEC_DAILY.ctl'
say _path_mge'/MERGE_CPTEC_DAILY.ctl'

#pull c
#'quit'

#
#'open '_path_cpc'/PRCP_CU_GAUGE_V1.0GLB_0.50deg.lnx.ctl'
#say _path_cpc'/PRCP_CU_GAUGE_V1.0GLB_0.50deg.lnx.ctl'
#
#'open '_path_mge'/MERGE_CPTEC_DAILY.ctl'
#say _path_mge'/MERGE_CPTEC_DAILY.ctl'
#
#'open '_path_mer'/merra2_total.ctl'
#say _path_mer'/merra2_total.ctl'
#
#'open '_path_chp'/chirps_daily.ctl'
#say _path_chp'/chirps_daily.ctl'
#
#'open '_path_inm'/inmet_stndata.ctl'
#say _path_inm'/inmet_stndata.ctl'
#
say
#pull c
#'q file'
#------------------------------------------#
#  Cria variável com data em forma de strg #
#              usando função               #
#------------------------------------------#
_diai='01'
_msi=subwrd(_nmon,_mesi)
#
_msf=subwrd(_nmon,_mesf)
_diaf=subwrd(ldy,_mesf)
if (_msf='FEB')
 if (_anof=1980|_anof=1984|_anof=1988|_anof=1992|_anof=1996|_anof=2000|_anof=2004|_anof=2008|_anof=2012|_anof=2016|_anof=2020|_anof=2024|_anof=2028|_anof=2032|_anof=2036|_anof=2040)
   _diaf=29
 endif
endif

#########################################################################
###                      Pega Tempo Inicial e Final                   ###
#########################################################################
#
'set time '_diai%_msi%_anoi
'q dims'
lin=sublin(result,5)
_ti=subwrd(lin,9)
#
'set time '_diaf%_msf%_anof
'q dims'
lin=sublin(result,5)
_tf=subwrd(lin,9)
#

say 'Tempo Inicial -> '_diai%_msi%_anoi' , '_ti
say 'Tempo Final   -> '_diaf%_msf%_anof' , '_tf

#pull c
#'quit'

##
#########################################################################
###               Inicia o Loop para gerar os dados                   ###
#########################################################################
#
# Loop Produtos de Precipitação
#
# _j=1
# while (_j<=1)
# while (_j<=3)
'set lat -35 -15'
'set lon -60 -30'
#
_t=_ti
while (_t<=_tf)
 'reset'
 'set gxout contour'
#   'set lat -60 15'
#   'set lon -90 -30'
 'set x 1'
 'set y 1'
 'set dfile 1'
 'set t '_t
 'q time'
  lin=subwrd(result,3)
  _dia=substr(lin,4,2)
  _mes=substr(lin,6,3)
  _ano=substr(lin,9,4)    
  ret=volta_mes()
  _data=_dia'/'_mm'/'_ano
  _mesano=_mm'/'_ano
  say
#  say '-------------------------------------------------------------------------'
  say 'data -> '_data
#  say '-------------------------------------------------------------------------'
#
#   'set lat '_lat
#   'set lon '_lon-360

  if (_dia=1)
     _ctmin15=0
     _ctmin18=0
     _ctmin21=0
     _ctmin23=0
     _ctmin1823=0
#
     _ctmax25=0
     _ctmax28=0
     _ctmax31=0
     _ctmax2528=0
#
     _cprec01=0
     _cprec011=0
     _cprec015=0
     _cprec510=0
  endif
#
  'set gxout stat'
  'set stnprint on'
#
#-----------------------------------------------------------------
#  Criterio TMIN
#-----------------------------------------------------------------
#
     say 'Criterio TMIN'
    'set dfile 3'
     if (_t=_ti)
      'd gr2stn(ave(tmin.3(z=1),t='_ti',t='_tf'),'_lon','_lat')'
       lin=sublin(result,10) ; _tmin=subwrd(lin,4)
       say 'TMIN AVE -> '_tmin
#       pull c
     endif
    'd gr2stn(tmin.3(z=1,time='_dia%_mes%_ano'),'_lon','_lat')'
     lin=sublin(result,17) ; ivar=subwrd(lin,6)
#    TMIN >= 15
     if (ivar >= 15);_ctmin15=_ctmin15+1;endif
#    TMIN >= 18
     if (ivar >= 18);_ctmin18=_ctmin18+1;endif
#    TMIN >= 21
     if (ivar >= 21);_ctmin21=_ctmin21+1;endif
#    TMIN >= 23
     if (ivar >= 23);_ctmin23=_ctmin23+1;endif
#    TMIN >= 18 & TMIN <= 23
     if (ivar >= 18 & ivar <= 23);_ctmin1823=_ctmin1823+1;endif
#     say 'TMIN ; ctmin15 ; ctmin18 ; ctmin21 ; ctmin23 ; ctmin1823  -> 'ivar' , '_ctmin15' , '_ctmin18' , '_ctmin21' , '_ctmin23' , '_ctmin1823
#
#-----------------------------------------------------------------
#  Criterio TMAX
#-----------------------------------------------------------------
#
     say 'Criterio TMAX'
    'set dfile 1'
     if (_t=_ti)
      'd gr2stn(ave(tmax.1(z=1),t='_ti',t='_tf'),'_lon','_lat')'
       lin=sublin(result,10) ; _tmax=subwrd(lin,4)
       say 'TMAX AVE -> '_tmax
#       pull c
     endif
    'd gr2stn(tmax.1(z=1,time='_dia%_mes%_ano'),'_lon','_lat')'
     lin=sublin(result,17) ; ivar=subwrd(lin,6)
#    TMAX >= 25
     if (ivar >= 25);_ctmax25=_ctmax25+1;endif
#    TMAX >= 28
     if (ivar >= 28);_ctmax28=_ctmax28+1;endif
#    TMAX < 25
     if (ivar < 31);_ctmax31=_ctmax31+1;endif
#    TMAX >= 25 & TMAX <= 28
     if (ivar >= 25 & ivar <= 28);_ctmax2528=_ctmax2528+1;endif
#     say 'TMAX ; ctmax25 ; ctmax28 ; ctmax31 ; ctmax2528 -> 'ivar' , '_ctmax25' , '_ctmax28' , '_ctmax31' , '_ctmax2528
#
#-----------------------------------------------------------------
#  Criterio PREC
#-----------------------------------------------------------------
#
     say 'Criterio PREC'
 
    'set dfile 4'
    'set x 1'
    'set y 1'
#    'q dims'
#     say result
     if (_t=_ti)
      'd gr2stn(sum(prec.4(z=1),t='_ti',t='_tf'),'_lon','_lat')'
       lin=sublin(result,10) ; _prec=subwrd(lin,4)
       say 'PREC SUM -> '_prec
#       pull c
     endif
    'd gr2stn(prec.4(z=1,time=12Z'_dia%_mes%_ano'),'_lon','_lat')'
     lin=sublin(result,17) ; ivar=subwrd(lin,6)
#    PREC > 0
     if (ivar > 0);_cprec01=_cprec01+1;endif
#    PREC > 0 e PREC <=1
     if (ivar > 0 & ivar <= 1);_cprec011=_cprec011+1;endif
#    PREC > 0 e PREC <=5
     if (ivar > 0 & ivar <= 5);_cprec015=_cprec015+1;endif
#    PREC > 5 e PREC <=10
     if (ivar > 5 & ivar <= 10);_cprec510=_cprec510+1;endif
#     say 'PREC ; cprec01 ; cprec011 ; cprec015 ; cprec510  -> 'ivar' , '_cprec01' , '_cprec011' , '_cprec015' , '_cprec510

#
#
     _file_out=_path_out'/dados_'_loc'_denge.txt'

#     if (_cab=1)
#       say 'Gerando Cabeçalho para '_loc' em '_mes%_ano
#       say 'File out -> '_file_out
#     endif

#
#    pull c
#    'quit'
#

       if (_cab=1)
         _outcab='DATA TMIN C15 C18 C21 C23 C1823 ND TMAX C25 C28 C-31 C2528 PREC P.1 P1 P5 P5.10 '
         say 'outcab -> '_outcab   
        '!printf "%7s %5s %5s %5s %5s %5s %5s %5s %5s %5s %5s %5s %5s %6s %5s %5s %5s %5s\n" '_outcab' > '_file_out
       endif

#    pull c
#    'quit'

#    '!rm -rf out_*.txt'

  _t=_t+1
  endwhile

  _outwri=_mesano' '_tmin' '_ctmin15' '_ctmin18' '_ctmin21' '_ctmin23' '_ctmin1823' '_diaf' '_tmax' '_ctmax25' '_ctmax28' '_ctmax31' '_ctmax2528' '_prec' '_cprec01' '_cprec011' '_cprec015' '_cprec510
  say 'outwri -> '_outwri  
 '!printf "%7s %5.1f%6.0f%6.0f%6.0f%6.0f%6.0f%6.0f %5.1f%6.0f%6.0f%6.0f%6.0f %6.1f%6.0f%6.0f%6.0f%6.0f %s\n" '_outwri' >> '_file_out 

 say 'Arquivo Gerado -> '_file_out 
 say '---------------------------------------------'


'quit'


#
#########################################################################
###                              FUNCOES                              ###
#########################################################################
#
#------------------------------------------#
# Ajustando data de decimal para string    #
#------------------------------------------#
function volta_mes()
if (_mes='JAN'); _mm='01' ; endif
if (_mes='FEB'); _mm='02' ; endif
if (_mes='MAR'); _mm='03' ; endif
if (_mes='APR'); _mm='04' ; endif
if (_mes='MAY'); _mm='05' ; endif
if (_mes='JUN'); _mm='06' ; endif
if (_mes='JUL'); _mm='07' ; endif
if (_mes='AUG'); _mm='08' ; endif
if (_mes='SEP'); _mm='09' ; endif
if (_mes='OCT'); _mm='10' ; endif
if (_mes='NOV'); _mm='11' ; endif
if (_mes='DEC'); _mm='12' ; endif

return geral


#------------------------------------------#
#  Encontra e marca ponto da lat lon       # 
#------------------------------------------#
#
function marca_regiao()

# desenhando os quadrados de cada regiao
'drawbox 270 280 -10 0'
'drawbox 210 270 -5 5'
'drawbox 190 240 -5 5'
'drawbox 160 210 -5 5'
'drawbox 298 313 -42 -32'

a=1
while (a<=5)
# Nome das Regioes
if (a=1);_lat_regiao=-15;_lon_regiao=275;_regiao='Nino1+2';endif
if (a=2);_lat_regiao=10;_lon_regiao=240;_regiao='Nino3';endif
if (a=3);_lat_regiao=-10;_lon_regiao=215;_regiao='Nino3.4';endif
if (a=4);_lat_regiao=10;_lon_regiao=185;_regiao='Nino4';endif
if (a=5);_lat_regiao=-45;_lon_regiao=302.5;_regiao='AAS';endif

# Sets color for the mark indicating location
  'set line 0'
  'set string 1 c 4'
  'set strsiz 0.15'
# Introduces world coordinates for Station
  lon1 = _lon_regiao
  lat1 = _lat_regiao
# Converts world coords to XY coords, it will be recalculated each time the map is changed 
  'q w2xy 'lon1' 'lat1
#  say result
# Loads the XY coords in x1 and y1
  x1 = subwrd(result,3)
  y1 = subwrd(result,6)
# Draws a marker at x1, y1 position with a selected size
#  'draw mark '9' 'x1' 'y1' '0.08
# Draws Station at x1+0.1 , y1 position (+0.1 is just an offset)
  'draw string 'x1+0.1' 'y1' '_regiao
a=a+1
endwhile 
return geral


