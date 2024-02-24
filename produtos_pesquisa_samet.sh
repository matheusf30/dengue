#!/bin/bash
#
###########################################################
#                                                         #
# Script Automático para executar os seguintes scripts    #
# operacionais:                                           #
#                                                         #
# 1) Indice de detecção de Frentes Frias - IFF            #
# 2) Indice de incidencia de Dengue                       #
#                                                         #
# Ex de como executar:                                    #
#                                                         #
# ./produtos_operacionais_gfs.sh 2022040112 84 0p50    #        
#                                                         #
#    Autor: Mario Quadro - CTMEt/IFSC    Data: 07/08/2020 #
#           Mario Quadro - PCAM/IFSC     Data: 07/04/2022 #
###########################################################
#
export LC_NUMERIC=en_US.UTF-8     ;# Comando para executar operacoes decimais
#
mt=(' ' 'JAN' 'FEB' 'MAR' 'APR' 'MAY' 'JUN' 'JUL' 'AUG' 'SEP' 'OCT' 'NOV' 'DEC')
dt=(' ' '31'  '28'  '31'  '30'  '31'  '30'  '31'  '31'  '30'  '31'  '30'  '31')
#
########################################################
# Definir os caminhos do scrips                        #
########################################################
#
path_iff=$HOME/scripts/iff/script_detecta_frente_fria_gfs
path_den=$HOME/scripts/scripts_dengue
path_gra=/opt/opengrads
path_png=/media/produtos/iff/figuras_ff_p17/oper
#path_dat=/media/dados/operacao
#
mkdir -p $path_iff
mkdir -p $path_den
#
#########################################################################
#  Define o Numero de Anos para processar os dados                      #
#########################################################################
#
if [ -z $1 ] 
then
# cria variável data do sistema
  echo " Entre com Parametros de Entrada:"
  echo "./produtos_operacionais_gfs.sh <anoi><mesi><diai><hori> <nhor> <res> "
  echo "Exemplo:  ./produtos_operacionais_gfs.sh 2022040112 84 0p50" 
  hhs=`date -u --date="0 days ago" +%H`
  #
  # Funcao para ajustar a hora
  #
  if [ $hhs -ge 05 -a $hhs -lt 11 ] 
  then 
   hh=00
  elif [ $hhs -ge 11 -a $hhs -lt 17 ] 
  then
   hh=06
  elif [ $hhs -ge 17 -a $hhs -lt 23 ] 
  then
   hh=12
  elif [ $hhs -ge 23 -o $hhs -lt 05 ] 
  then 
   hh=18
  fi	
  datai=`date -u --date="0 days ago" +%Y%m%d`"$hh" 
else
  datai=$1
fi

#
if [ -z $2 ] 
then
# cria variável data do sistema
  echo " Entre com Parametros de Entrada:"
  echo "./produtos_operacionais_gfs.sh <anoi><mesi><diai><hori> <nhor> <res>  "
  echo "Exemplo:  ./produtos_operacionais_gfs.sh 2022040112 84 0p50" 
  nhor=84
else
  nhor=$2
fi
#
if [ -z $3 ] 
then
# cria variável data do sistema
  echo " Entre com Parametros de Entrada:"
  echo "./produtos_operacionais_gfs.sh <anoi><mesi><diai><hori> <nhor> <res>  "
  echo "Exemplo:  ./produtos_operacionais_gfs.sh 2022040112 84 0p50" 
  res=0p50
else
  res=$3
fi
#
echo  " Data Inicial    -> "$datai
echo  " Numero de Horas -> "$nhor
echo  " Resolucao       -> "$res
#
#########################################################################
#  Roda o Script do Indice de detecção de Frentes Frias - IFF           #
#########################################################################
#
cd $path_iff
echo $path_gra/opengrads -bpc "run detecta_frente_fria_gfs.gs $datai $nhor $res"
$path_gra/opengrads -bpc "run detecta_frente_fria_gfs.gs $datai $nhor $res"
cd ${path_png}
pwd
ls
cnt=`ls *.png | wc -l | awk '{print $1 }'`
echo "No de arquivos na pasta -> "$ver_nar
for (( i = 0; i < $cnt; i++ ))
do
  j=$((i+1))
  arq=`ls mapa_*.png | head -$j | tail -1 | awk '{print $1 }'`
  echo "Arquivo -> "$arq
  convert $path_iff/Logo_IFSC.png -geometry x80 $path_iff/resize_Logo_IFSC.png
  #echo $path_iff/resize_Logo_IFSC.png
  #exit  
  composite -dissolve 100% -geometry +512+612 $path_iff/resize_Logo_IFSC.png ${arq} new_${arq}
  mv new_${arq} ${arq}
done
#
#########################################################################
#  Roda o Script do Indice de Incidencia de Dengue                      #
#########################################################################
#
cd $path_den
#echo $path_gra/opengrads -bpc "run xxxxxxxxxxxxxxxxxx.gs $datai $nhor $res"
#$path_gra/opengrads -bpc "run xxxxxxxxxxxxxxxxxxxx.gs $datai $nhor $res"
#
#########################################################################
#  Gera animacao                                                  #
#########################################################################
#
cd $path_png
echo 
echo "Gera Animação"
/usr/bin/convert -delay 100 -loop 0 mapa_iff_*.png anima_iff.gif
#
#########################################################################
#  Copia Imagens para a página                                          #
#########################################################################
#
echo 
echo "Copia imagens para página"
scp -r $path_png meteoro@172.16.128.48:/opt/lampp/htdocs/climenv/produtos_alunos/iff
scp -r $path_png meteoper@172.16.0.111:/opt/lampp/htdocs/climenv/produtos_alunos/iff
#
rm -rf nohup.out
#
#

