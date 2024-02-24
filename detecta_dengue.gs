function geral(args)
'reinit'
#
#########################################################################
### Script Automático monitorar as condições ambientais para          ### 
### a proliferaçõa do Aedes.                                          ### 
### Utiliza o GFS do NCEP com previsões ate 84 horas.                 ###
###                                                                   ###
###                                                                   ###
### Elaborado por; Matheus Souza e Mario Quadro                       ###
###                                                                   ###
###                                                                   ###
###       Para rodar :                                                ###
###                                                                   ###
###               "run detecta_dengue.gs YYYYMMDDHH(i) nhor res"      ###
###                                   Adaptado em:   07/10/2022       ###
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
_nhor=subwrd(args,2)
#
_res=subwrd(args,3)
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
_path_scr='/home/meteoper/scripts/iff/script_detecta_frente_fria_gfs'
#_path_dat='/home/iff/Documentos/mestrado/dado/gfs'
#_path_dat='/media/iff/hd_extra/mestrado/frentefria/dado/gfs' 
#_path_dat='/media/hd2tb/dados/pesquisa/cfsr'
_path_dat='/media/dados/operacao/gfs'
_path_png='/media/produtos/iff'
_path_lib='/usr/share/grads'
*
#
say 'Data da Execucao -> '_anoi%_mesi%_diai%_hori
#
'open '_path_dat'/'_res'/'_anoi%_mesi'/'_datai'/gfs_'_datai'.ctl'
say 'Arquivo Aberto -> '_path_dat'/'_res'/'_anoi%_mesi'/'_datai'/gfs_'_datai'.ctl'
#
'set mpdset brmap_hires'
'run '_path_lib'/define_colors.gs'
#
#pull c
#'quit'

*************************************************************************************
* Define a porcentagem de pontos no gráfico de Detecção da FF
*************************************************************************************
*
_porlim=17;# Porcentagem de pontos Limite para detectar a condição de proliferacao do mosquito
*
*************************************************************************************
* Define Arquivos de Saída
*************************************************************************************
*
_path_png=_path_png'/figuras_ff_p'_porlim
'!mkdir -p '_path_png
'!mkdir -p '_path_png'/oper'
'!rm -rf '_path_png'/oper/*.png'
#
#
_path_out=_path_png'/casos_ff_p'_porlim
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
#Define ultimo DATA DO ARQUIVO
##############################################
#
  'set time '_hori'Z'_diai%_msi%_anoi
  'q dims'
   _tinic=sublin(result,5)
   _tinic=subwrd(_tinic,9)
#
  'set t '_nhor
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

say 'No de tempos -> '_ntimes

#pull c
#'quit'

_t=_tinic+1
_cont=1
#
while (_t <= _ntimes)
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
'set lon -76 -36'
'set lat -50 -15'
#'set lon -55 -47'
#'set lat -30 -25'
'set t '_t
#'define a=((abs(vgrd10m)-vgrd10m)/2)*-1'
#'define b=((abs(vgrd10m(t+1))+vgrd10m(t+1))/2)'
#'define c=((abs(vgrd10m(t+2))+vgrd10m(t+2))/2)'
#'define d=((abs(vgrd10m(t+3))+vgrd10m(t+3))/2)'
#'define e=((abs(vgrd10m(t+4))+vgrd10m(t+4))/2)'
'define a=((abs(vgrd10m(t-1))-vgrd10m(t-1))/2)*-1'
'define b=((abs(vgrd10m)+vgrd10m)/2)'
'define c=((abs(vgrd10m(t+1))+vgrd10m(t+1))/2)'
'define d=((abs(vgrd10m(t+2))+vgrd10m(t+2))/2)'
'define e=((abs(vgrd10m(t+3))+vgrd10m(t+3))/2)'
*************************************************************************************
* Critérios do Script
**************************************************************************************
*
'q time'
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
*
**************************************************************************************
* define a diminuição de tmp2meratura de um periodo para outro
**************************************************************************************
#'define t1=(tmp2m-tmp2m(t+4))'
'define t1=(tmp2m(t-1)-tmp2m(t+3))'
#'define t2=(tmp2m(t+1)-tmp2m(t+5))'
#'define t3=(tmp2m(t+2)-tmp2m(t+6))'
#'define t4=(tmp2m(t+3)-tmp2m(t+7))'
*
**************************************************************************************
* seleciona as áreas onde houve queda de tmp2meratura
**************************************************************************************
*
'define at1=(abs(t1)+t1)/2'
#'define at2=(abs(t2)+t2)/2'
#'define at3=(abs(t3)+t3)/2'
#'define at4=(abs(t4)+t4)/2'
*
**************************************************************************************
* Critérios do Script
* a*b -> Seleciona áreas aonde o vento girou de norte p/ sul
* a*b*c*d*e -> A partir do criterio anterior, se o vento permaneceu de sul por um dia
* a*b*c*d*e*at1 -> A partir do criterio anterior, se a tmp2meratura diminuiu 24h depois
*		   da passagem da frente.
**************************************************************************************
*
'c'
'set gxout grfill'
'set xlopts 1 1 0.16'
'set ylopts 1 1 0.16'
'set grads off'
'set rgb 80 245 245 245'
'set grid on 1 80'
*
'define iff=sqrt((a*-1)*b*(a/a)*(b/b)*(c/c)*(d/d)*(e/e)*at1)'
'set gxout stat'
'd iff'
lin=sublin(result,8)
_vmax=subwrd(lin,5)
'define iffn=10*iff/'_vmax
#
'set gxout grfill'
'set grads off'
#'set ccols 0 23  24  25  27  28  29  33  34  35  37  38  39  43  44  45  46  47  48  49  59 '
'set ccols 0  43  44  45  47  48  49  33  34  35  37  38  39  23  24  25  26  27  28  29  0'
'set clevs   1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0 5.5 6.0 6.5 7.0 7.5 8.0 8.5 9.0 9.5 10.'
'd iffn'
#say _path_lib'/cbarn.gs'
'run '_path_lib'/cbarn.gs 1.0 0 4.25 0.7'

_k=1
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
'draw title Indice Normalizado de Frentes Frias (IFFN) \ Previsao Para -> '_ht'Z de 'dd'/'_mm'/'yy
'set strsiz 0.13'
'draw string 2.25 1.1 FRACO'
'draw string 4.25 1.1 MODERADO'
'draw string 6.25 1.1 INTENSO'
'set strsiz 0.11'
'set string 15 c 6'
'draw string 4.25 0.3 Fonte: PCAM/IFSC - Dados: Modelo GFS/NCEP '_res 
'!mkdir -p '_path_png'/'yy
'!mkdir -p '_path_png'/'yy'/'_mm
#
'set ccolor 15'
'set gxout contour'
'set cint 4'
'd PRMSLmsl/100'
'printim '_path_png'/oper/mapa_iff_'_ncont'.png white'
'printim '_path_png'/'yy'/'_mm'/mapa_iff_'yy%_mm%dd%_ht'.png white'
 say 'Figura Gerada -> '_path_png'/oper/mapa_iff_'_ncont'.png'
# say 'Figura Gerada -> '_path_png'/'yy'/'_mm'/mapa_iff_'yy%_mm%dd%_ht'.png'
#pull c
#'quit'


#'draw title Frentes Frias Selecionadas \ Criterio Vento (10m) e Temperatura (2m) \ Data -> 'dia
#'draw xlab Fonte: Modelo Global GFS 0.25'
#'printim '_path_png'/'_anoi%_mesi'/mapa_ff_'dd%_mm%yy%_%hh'.png white'
#say 'Figura Gerada -> '_path_png'/'_anoi%_mesi'/mapa_ff_'dd%_mm%yy%_%hh'.png'
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


