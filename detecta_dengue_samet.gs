function geral(args)
'reinit'
#
#########################################################################
### Script Automático monitorar as condições ambientais para          ### 
### a proliferaçõa do Aedes.                                          ### 
### Utiliza os dados diários do SAMET.                                ###
###                                                                   ###
###                                                                   ###
### Elaborado por; Matheus Souza e Mario Quadro                       ###
###                                                                   ###
###                                                                   ###
###       Para rodar :                                                ###
###                                                                   ###
###               "run detecta_dengue.gs YYYYMMDDHH(i) nday"          ###
###                                   Adaptado em:   03/03/2023       ###
###                                                                   ###
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
_hori=substr(_datai,9,2)
#
_nday=subwrd(args,2)
#
#_res=subwrd(args,3)
#
#------------------------------------------#
#  Cria variável com data em forma de strg #
#              usando função               #
#------------------------------------------#
ret=arruma_mes(_mesi)
_msi=_mes_string
#
#
#########################################################################
###                  Define PAths                    ###
#########################################################################
#
_path_scr='/home/meteoper/scripts/scripts_dengue'
#_path_dat='/home/iff/Documentos/mestrado/dado/gfs'
#_path_dat='/media/iff/hd_extra/mestrado/frentefria/dado/gfs' 
#_path_dat='/media/hd2tb/dados/pesquisa/cfsr'
_path_dat='/media/dados/operacao/samet/daily'
_path_png='/media/produtos/dengue'
_path_lib='/usr/share/grads'
*
'!mkdir -p '_path_png
#
say 'Data da Execucao -> '_anoi%_mesi%_diai%_hori
#
'open '_path_dat'/TMAX/SAMeT_CPTEC_TMAX.ctl'
say 'Arquivo Aberto -> '_path_dat'/TMAX/SAMeT_CPTEC_TMAX.ctl'
#
'open '_path_dat'/TMED/SAMeT_CPTEC_TMED.ctl'
say 'Arquivo Aberto -> '_path_dat'/TMED/SAMeT_CPTEC_TMED.ctl'
#
'open '_path_dat'/TMIN/SAMeT_CPTEC_TMIN.ctl'
say 'Arquivo Aberto -> '_path_dat'/TMIN/SAMeT_CPTEC_TMIN.ctl'
#
'set mpdset brmap_hires'
'set parea 0.5 10.5 1.2 7.8'
'run '_path_lib'/define_colors.gs'
#
#pull c
#'quit'

*************************************************************************************
* Define a porcentagem de pontos no gráfico de Detecção da FF
*************************************************************************************
*
_porlim=17;# Porcentagem de pontos Limite para detectar a condição de proliferacao do mosquito
_tmplim=15;# Limiar da temperatura para detectar a possibilidade de proliferacao
*
*************************************************************************************
* Define Arquivos de Saída
*************************************************************************************
*
#_path_png=_path_png'/figuras_dengue_p'_porlim
_path_png=_path_png'/figuras_dengue_samet'
'!mkdir -p '_path_png
'!mkdir -p '_path_png'/oper'
'!rm -rf '_path_png'/oper/*.png'
#
say _path_png'/oper'
#
#_path_out=_path_png'/casos_dengue_p'_porlim
_path_out=_path_png'/casos_dengue_samet' 
'!mkdir -p '_path_out

#'!mkdir -p '_path_png'/'_anoi%_mesi
*************************************************************************************
* Define as variaveis para o calculo
* a -> Seleciona areas de vento no quadrante norte (t=-1)
* b -> Seleciona areas de vento no quadrante sul (t=2)
* c -> Seleciona areas de vento no quadrante sul (t=3)
* d -> Seleciona areas de vento no quadrante sul (t=4)
* e -> Seleciona areas de vento no quadrante sul (t=5)
*************************************************************************************
*
##########################################
#Define a DATA DO ARQUIVO
##############################################
#
  'set time '_hori'Z'_diai%_msi%_anoi
  'q dims'
   _tinic=sublin(result,5)
   _tinic=subwrd(_tinic,9)
   _tfinal=_tinic+_nday-1
#
  'set t '_tfinal
  'q dims'
   say result
   _tlast=sublin(result,5)
   time=subwrd(_tlast,6)
   _horf=substr(time,1,2)
   _diaf=substr(time,4,2)
   _mesf=substr(time,6,3)
    ret=arruma_mes(_mesf)
   _msf=_mes_string
   _anof=substr(time,9,4)
#
   _tlast=subwrd(_tlast,9)
#
   say 'Tempo Inicial -> '_tinic
   say 'Tempo Final   -> '_tlast
#

say 'Tempo Inicial, Tempo Final -> '_hori'Z'_diai%_msi%_anoi' (t='_tinic') a 18Z'_diaf%_msf%_anof' (t='_tlast')'

#_ntimes=(_tlast/3)+1
_ntimes=(_tlast/3)-2
_ntimes=(_tfinal-_tinic)+1

say 'No de tempos -> '_ntimes

#pull c
#'quit'

_t=_tinic
_cont=1
#
while (_t <= _tfinal)
*
if (_cont < 10)
  _ncont='0'_cont
else
   _ncont=_cont
endif

'c'
*************************************************************************************
* Define a área do Mapa e os critéros do vento
*************************************************************************************
*
#'set lon -76 -36'
#'set lat -50 -15'
'set lon -54.5 -47.5'
'set lat -29.5 -25.5'
'set t '_t
*************************************************************************************
* Critérios do Script
**************************************************************************************
*
'q time'
say result
lin=sublin(result,1)
dia=subwrd(lin,3)
hh=substr(dia,1,3)
_hh=substr(dia,1,2)
dd=substr(dia,4,2)
mm=substr(dia,6,3)
yy=substr(dia,9,4)
#

_ht=_hh
#if (_ht<10);_ht='0'_ht;endif
#

#
if (_mm="JAN" & _dd="01")
  '!rm -rf '_arqout
endif
_mmm=mm
ret=month()
*
say
say 'Time-> '_t' , Data-> '_ht'Z de 'dd'/'_mm'/'yy

#pull c
#'quit'

*
**************************************************************************************
* define se a temperatura é maior que o limiar estabelecido
**************************************************************************************
#'define t1=(tmax-273.15-'_tmplim')'
'define t1=(tmax-'_tmplim')'
*
**************************************************************************************
* seleciona as áreas onde houve tempmeratura maior que o limiar estabelecido
**************************************************************************************
*
'define at1=(abs(t1)+t1)/2'
*
'c'
'set gxout grfill'
'set xlopts 1 1 0.14'
'set ylopts 1 1 0.14'
'set grads off'
'set rgb 80 245 245 245'
'set grid off'
#'set grid on 1 80'
*
'define idengue=at1/at1'
#'d at1*idengue'
#'set gxout grid'
#'d at1*idengue'
'set gxout stat'
'd at1*idengue'

#pull c
#'quit'


#say result
lin=sublin(result,9)
_vmax=subwrd(lin,6)
#
if (_vmax >= 10)
  _nvmax=_vmax
else
  _nvmax=10
endif
#
say 'vmax -> '_nvmax
'define idenguen=10*at1*idengue/'_nvmax
#
'set gxout grfill'
'set grads off'
'set ccols 0  43  44  45  47  48  49  33  34  35  37  38  39  23  24  25  26  27  28  29  0'
'set clevs   1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0 5.5 6.0 6.5 7.0 7.5 8.0 8.5 9.0 9.5 10.0'
'd idenguen'
#pull c
#'quit'
#say _path_lib'/cbarn.gs'
'run '_path_lib'/cbarn.gs 1.0 0 5.5 0.40'
#'run '_path_lib'/cbarn.gs'

_k=11
while (_k <= 10)

  ret=definearea()

  _lat=_lati ; _lon=_loni
  ret=convert_w2xy()
  _xlo=_xpos ; _ylo=_ypos

  _lat=_latf ; _lon=_lonf
  ret=convert_w2xy()
  _xhi=_xpos ; _yhi=_ypos

#  ret=disparea()
  _lon=_lonf ; _lat=_latf
  ret=convert_w2xy()
   _amen=0.15
#  'draw recf '_xpos-(_amen*2)' '_ypos-(_amen*2)' '_xpos' '_ypos
  'set string 1 c 6'
#  'draw string '_xpos-_amen' '_ypos-_amen' '_area
_k=_k+1
endwhile

#'run '_path_lib'/cbarn.gs'
'draw title Indice Normalizado de Proliferacao de Aedes aegypti (Limiar '_tmplim'C)\ Previsao Para -> '_ht'Z de 'dd'/'_mm'/'yy
'set strsiz 0.13'
'draw string 2.75 0.85 FRACO'
'draw string 5.80 0.85 MODERADO'
'draw string 8.25 0.85 INTENSO'
'set strsiz 0.11'
'set string 15 r 6'
'draw string 10.9 0.1 Fonte: PCAM/IFSC - Dados: Produto SAMeT '_res 
'!mkdir -p '_path_png'/'yy
'!mkdir -p '_path_png'/'yy'/'_mm
#
#pull c
#'quit'
#'set ccolor 15'
#'set gxout contour'
#'set cint 4'
#'d PRMSLmsl/100'
'printim '_path_png'/oper/mapa_idengue_'_ncont'.png white'
'printim '_path_png'/'yy'/'_mm'/mapa_idengue_'yy%_mm%dd%_ht'.png white'
# say 'Figura Gerada -> '_path_png'/oper/mapa_idengue_'_ncont'.png'
 say 'Figura Gerada -> '_path_png'/'yy'/'_mm'/mapa_idengue_'yy%_mm%dd%_ht'.png'
pull c
#'quit'
*
* Gera estatísticas
*
_k=11 
while (_k <= 10)

  ret=definearea()

  _arq_out=_path_out'/casos_'yy'_areas/casos_'yy'_p'_porlim'_'_area'.txt' 
  _csv_out=_path_out'/casos_'yy'_areas/casos_'yy'_p'_porlim'_'_area'.csv' 
  '!mkdir -p '_path_out'/casos_'yy'_areas'
#
  _arq_lit=_path_out'/casos_'yy'_p'_porlim'_AL.txt'
  _csv_lit=_path_out'/casos_'yy'_p'_porlim'_AL.csv'
#
  _arq_con=_path_out'/casos_'yy'_p'_porlim'_AC.txt'
  _csv_con=_path_out'/casos_'yy'_p'_porlim'_AC.csv'
#
  _arq_tot=_path_out'/casos_'yy'_p'_porlim'.txt'
  _csv_tot=_path_out'/casos_'yy'_p'_porlim'.csv'


  ret=statistics()
*
#pull c


  if (mm="JAN" & dd="01" & _ht="00")
   _outwri='BOX DATA HOR POR IFFN IFF'
   '!printf "%3s%11s%4s%5s%5s%5s %s\n" '_outwri' > '_arq_out
   '!printf "%3s%11s%4s%5s%5s%5s %s\n" '_outwri' > '_arq_tot
   '!printf "%3s%11s%4s%5s%5s%5s %s\n" '_outwri' > '_arq_lit
   '!printf "%3s%11s%4s%5s%5s%5s %s\n" '_outwri' > '_arq_con
  endif
#
  _datprn=dd'/'_mm'/'yy
  _horprn=_ht'Z'
#
  if(_porcnt >= _porlim)
    fmt = '%5.1f'
    _fviffn = math_format(fmt,_viffn)
    _fviff = math_format(fmt,_viff)

    _fporcnt = math_format(fmt,_porcnt)
    _outwri=_area' '_datprn' '_horprn' '_fporcnt' '_fviffn' '_fviff


#    say 'outwri -> '_outwri

#pull c 
#'quit'

    '!printf "%3s%11s%4s%5.1f%5.1f%5.1f %s\n" '_outwri' >> '_arq_out
    '!printf "%3s%11s%4s%5.1f%5.1f%5.1f %s\n" '_outwri' >> '_arq_tot
    _varea=substr(_area,1,2)
    if(_varea = "AL")  
      '!printf "%3s%11s%4s%5.1f%5.1f%5.1f %s\n" '_outwri' >> '_arq_lit
    endif
    if(_varea = "AC")  
      '!printf "%3s%11s%4s%5.1f%5.1f%5.1f %s\n" '_outwri' >> '_arq_con
    endif

#    say fmt' of 'v' = 'rc
#   '!echo '_area' 'yy%_mm%dd%_hh' '_fporcnt' '_fvmax' >> '_arq_out

#
##############################################
# Copia o arquivo gerdo para um csv e 
# Substitui um ou mais espaços por ponto e vírgula
##############################################
#


    say 'Arquivo Gerado -> '_arq_out
    say 'Arquivo Gerado -> '_arq_tot

  endif

  if(_t = _tlast)
    '!cp -rf '_arq_out' '_csv_out
    '!sed -i "s/ \+/;/g" '_csv_out  
    '!sed -i "s/;BOX/BOX/g" '_csv_out
#
    '!cp -rf '_arq_lit' '_csv_lit
    '!sed -i "s/ \+/;/g" '_csv_lit  
    '!sed -i "s/;BOX/BOX/g" '_csv_lit
#
    '!cp -rf '_arq_con' '_csv_con
    '!sed -i "s/ \+/;/g" '_csv_con 
    '!sed -i "s/;BOX/BOX/g" '_csv_con
#
    '!cp -rf '_arq_tot' '_csv_tot
    '!sed -i "s/ \+/;/g" '_csv_tot 
    '!sed -i "s/;BOX/BOX/g" '_csv_tot
  endif


_k=_k+1
endwhile


*
_cont=_cont+1
_t=_t+1
endwhile

'quit'

return 'ok'

#
##############################################
function definearea()
##############################################
#
# Convert screen positions to grid coordinates
  _deltalon=8
  _deltalat=5

  if(_k=1)
   _lati=-45.0 ; _latf=_lati+_deltalat ; _loni=-69.0 ; _lonf=_loni+_deltalon ; _area=AL1    ;# Área AL1
  endif
  if(_k=2)
   _lati=-40.0 ; _latf=_lati+_deltalat ; _loni=-63.0 ; _lonf=_loni+_deltalon ; _area=AL2    ;# Área AL2
  endif
  if(_k=3)
   _lati=-35.0 ; _latf=_lati+_deltalat ; _loni=-58.0 ; _lonf=_loni+_deltalon ; _area=AL3    ;# Área AL3
  endif
  if(_k=4)
   _lati=-30.0 ; _latf=_lati+_deltalat ; _loni=-55.0 ; _lonf=_loni+_deltalon  ; _area=AL4   ;# Área AL4
  endif
  if(_k=5)
   _lati=-25.0 ; _latf=_lati+_deltalat ; _loni=-48.5 ; _lonf=_loni+_deltalon  ; _area=AL5   ;# Área AL5
  endif
  if(_k=6)
   _lati=-40.0 ; _latf=_lati+_deltalat ; _loni=-71.0 ; _lonf=_loni+_deltalon ; _area=AC1    ;# Área AC1
  endif
  if(_k=7)
   _lati=-35.0 ; _latf=_lati+_deltalat ; _loni=-66.0 ; _lonf=_loni+_deltalon ; _area=AC2    ;# Área AC2
  endif
  if(_k=8)
   _lati=-30.0 ; _latf=_lati+_deltalat ; _loni=-63.0 ; _lonf=_loni+_deltalon ; _area=AC3    ;# Área AC3
  endif
  if(_k=9)
   _lati=-25.0 ; _latf=_lati+_deltalat ; _loni=-56.5 ; _lonf=_loni+_deltalon ; _area=AC4    ;# Área AC4
  endif
if(_k=10)
   _lati=-25.0 ; _latf=_lati+_deltalat ; _loni=-64.5 ; _lonf=_loni+_deltalon ; _area=AC5    ;# Área AC5
  endif


return

#
##############################################
function statistics()
##############################################
#
# Convert screen positions to grid coordinates

'c'
#'set gxout grid'
'set lat '_lati' '_latf
'set lon '_loni' '_lonf
#'d iffn'
'set gxout stat'
'd iff'
lin=sublin(result,8)
_viff=subwrd(lin,5)
#

'd iffn'
#say result
lin=sublin(result,7)
_undefc=subwrd(lin,4)
_validc=subwrd(lin,8)
_totcnt=_undefc+_validc
_porcnt=(_validc/_totcnt)*100
lin=sublin(result,8)
_viffn=subwrd(lin,5)

#say 'Undef , Valid , Porcentage -> '_undefc' , '_validc' , '_porcnt
return

#
##############################################
function convert_w2xy()
##############################################
#
# Convert screen positions to grid coordinates
#
'q w2xy '_lon' '_lat
#say result
_xpos = subwrd(result,3)
_ypos = subwrd(result,6)
# Round the grid values to the nearest integer
#_gx = math_nint(_xpos)
#_gy = math_nint(_ypos)
#say 'Posicao x -> '_xpos
#say 'Posicao y -> '_ypos
return

#
##############################################
function disparea()
##############################################
#
# FUNCAO PARA DAR O DISPLAY DOS CALCULOS NA TELA
#
'set line 1'
'draw rec '_xlo' '_ylo' '_xhi' '_yhi
*'set line '_clin
*'draw rec '_xlo' '_ylo' '_xhi' '_yhi
*'draw string '_xpos' '_ypos' '_dispvalue
return

#
##############################################
function month()
##############################################
#
if (_mmm='JAN') ;_mm=01; endif
if (_mmm='FEB') ;_mm=02; endif
if (_mmm='MAR') ;_mm=03; endif
if (_mmm='APR') ;_mm=04; endif
if (_mmm='MAY') ;_mm=05; endif
if (_mmm='JUN') ;_mm=06; endif
if (_mmm='JUL') ;_mm=07; endif
if (_mmm='AUG') ;_mm=08; endif
if (_mmm='SEP') ;_mm=09; endif
if (_mmm='OCT') ;_mm=10;endif
if (_mmm='NOV') ;_mm=11;endif
if (_mmm='DEC') ;_mm=12;endif

return

#
#------------------------------------------#
# Ajustando data de decimal para string    #
#------------------------------------------#
function arruma_mes(mes)
_mes_decimal=subwrd(mes,1)
if (_mes_decimal = 01 ); _mes_string='JAN' ;  endif
if (_mes_decimal = 02 ); _mes_string='FEB' ;  endif
if (_mes_decimal = 03 ); _mes_string='MAR' ;  endif
if (_mes_decimal = 04 ); _mes_string='APR' ;  endif
if (_mes_decimal = 05 ); _mes_string='MAY' ;  endif
if (_mes_decimal = 06 ); _mes_string='JUN' ;  endif
if (_mes_decimal = 07 ); _mes_string='JUL' ;  endif
if (_mes_decimal = 08 ); _mes_string='AUG' ;  endif
if (_mes_decimal = 09 ); _mes_string='SEP' ;  endif
if (_mes_decimal = 10 ); _mes_string='OCT' ;  endif
if (_mes_decimal = 11 ); _mes_string='NOV' ;  endif
if (_mes_decimal = 12 ); _mes_string='DEC' ;  endif

return geral


