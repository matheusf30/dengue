#!/bin/bash
#
######################################################################
### Esse script tem como objetivo gerar a Serie temporal dos dados ### 
### de temperatura e Produto de Precipitacao SAMET/MERGE. É gerada ### 
### uma tabela para o Estudo da CLeusa/Matheus                     ###
###                                                                ###  
### Para EXECUTAR:                                                 ###
### ./roda_geral_serie_temporal_dengue.sh                          ###  
###                                                                ###
###                                                                ###
###                                                                ###  
### Elaborado Por: MARIO QUADRO  Adaptado por: MARIO QUADRO        ###
### FEB, 20th 2023                                                 ###
######################################################################
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
path_scr=$HOME/scripts/scripts_dengue
path_dat=$path_scr/out_data
#path_mer=/media/dados/operacao/merge/CDO.MERGE       ;#path merge Cluster
#path_sam=/media/dados/operacao/samet                  ;#path Samet cluster
path_mer=/dados/operacao/merge/CDO.MERGE              ;#path merge sifapsc
path_sam=/dados/operacao/samet/clima/                  ;#path Samet sifapsc
#
mkdir -p $path_scr
mkdir -p $path_dat
#
#rm -rf $path_dat/*.txt $path_dat/*.csv
#
list_estac=$path_scr/lista_cidades_pontoscentrais_sc.csv
#arq_mer=${path_mer}/MERGE_CPTEC_DAILY_PREC_SB_2000_2022.nc  ;#file merge Cluster
arq_mer=${path_mer}/MERGE_CPTEC_DAILY_SB_PREC_2000_2022.nc  ;#file merge Sifap
#
arq_tme=${path_sam}/TMED/SAMeT_CPTEC_DAILY_TMED_SB_2000_2022.nc
arq_tma=${path_sam}/TMAX/SAMeT_CPTEC_DAILY_TMAX_SB_2000_2022.nc
arq_tmi=${path_sam}/TMIN/SAMeT_CPTEC_DAILY_TMIN_SB_2000_2022.nc
#
#########################################################################
#  Define Parametros
#########################################################################
#
rodscr=s
arqtime=$path_scr/time_exec.txt
#
#echo "Tempo Inicial: " > ${arq_time}
#date >> ${arq_time}
#
#########################################################################
###                     Define valor indefinido                   ###
#########################################################################
#
#undef=-9999.0
# undef=NaN
#
########################################################
#  Define a Estacao Inicia (esti) e o Número de        # 
#  Estacoes (nest) a ser gerarado os dados             #
########################################################
#
#
esti=2
nest=`wc -l $list_estac | awk '{ print $1}'`
#
echo " Arq. Listagem das Estacoes  -> "$list_estac
echo " Estação Inicial             -> "$esti
echo " No de Estacoes              -> "$nest
echo " Arquivo de dados MERGE      -> "$arq_mer
echo " Arquivo de dados SAMET TMED -> "$arq_tme
#
mer_out=$path_dat/merge_all.txt
tmi_out=$path_dat/samet_tmin_all.txt
tme_out=$path_dat/samet_tmed_all.txt
tma_out=$path_dat/samet_tmax_all.txt
#
mer_csv=$path_dat/merge_all.csv
tmi_csv=$path_dat/samet_tmin_all.csv
tme_csv=$path_dat/samet_tmed_all.csv
tma_csv=$path_dat/samet_tmax_all.csv
#
#
########################################################
#  Faz o loop p/ Executar o CDO para os dados do MERGE #
########################################################
#
#esti=$((nest+1))
#
for (( j = ${esti}; j <= ${nest}; j++ ))
#for (( j = ${esti}; j <= 30; j++ ))
do
 
  cod=`head -$j $list_estac | tail -1 | cut -d"," -f2`
  lat=`head -$j $list_estac | tail -1 | cut -d"," -f3`
  lon=`head -$j $list_estac | tail -1 | cut -d"," -f4`
  #est=`head -$j $list_estac | tail -1 | cut -d"," -f7`
  mun=`head -$j $list_estac | tail -1 | cut -d"," -f5`
  #
  mer_dat=$path_dat/merge_${cod}.txt
  sam_tmi=$path_dat/samet_tmin_${cod}.txt
  sam_tme=$path_dat/samet_tmed_${cod}.txt
  sam_tma=$path_dat/samet_tmax_${cod}.txt
  #
  echo "-----------------------------------------------------------"
  echo "Localidade, Latitude, Longitude -> "$mun" , "$lat" , "$lon
  cd $path_scr
  pwd
  #
  # Gera arquivo das datas
  #
  if [ ${j} -eq ${esti} ] 
  then
   # prec merge
   echo "cdo -outputtab,date,lon,lat -remapnn,"lon=${lon}_lat=${lat}" $arq_mer" 
   #cdo -outputtab,date,lon,lat -remapnn,"lon=${lon}_lat=${lat}" $arq_mer > ${mer_out}
   cdo -outputtab,date -remapnn,"lon=${lon}_lat=${lat}" $arq_mer > ${mer_out}
   sed -i 's/.$//g' ${mer_out}             ;# retira a última linha do 
   # tmed samet
   echo "cdo -outputtab,date,lon,lat -remapnn,"lon=${lon}_lat=${lat}" $arq_tme"
   #cdo -outputtab,date,lon,lat -remapnn,"lon=${lon}_lat=${lat}" $arq_tme > ${tme_out}
   cdo -outputtab,date -remapnn,"lon=${lon}_lat=${lat}" $arq_tme > ${tme_out}
   sed -i 's/.$//g' ${tme_out}             ;# retira a última linha do 
   # tmin samet
   echo "cdo -outputtab,date,lon,lat -remapnn,"lon=${lon}_lat=${lat}" $arq_tmi"
   #cdo -outputtab,date,lon,lat -remapnn,"lon=${lon}_lat=${lat}" $arq_tmi > ${tmi_out}
   cdo -outputtab,date -remapnn,"lon=${lon}_lat=${lat}" $arq_tmi > ${tmi_out}
   sed -i 's/.$//g' ${tmi_out}             ;# retira a última linha do 
   # tmax samet
   echo "cdo -outputtab,date,lon,lat -remapnn,"lon=${lon}_lat=${lat}" $arq_tma"
   #cdo -outputtab,date,lon,lat -remapnn,"lon=${lon}_lat=${lat}" $arq_tma > ${tma_out}
   cdo -outputtab,date -remapnn,"lon=${lon}_lat=${lat}" $arq_tma > ${tma_out}
   sed -i 's/.$//g' ${tma_out}             ;# retira a última linha do 
  fi
  #
  # Gera arquivo das datas MERGE
  #
  #cdo -outputtab,date,lon,lat,value -remapnn,"lon=${lon}_lat=${lat}" $arq_mer > $mer_dat
  cdo -outputtab,value -remapnn,"lon=${lon}_lat=${lat}" $arq_mer  > ${mer_dat}
  sed -i "s/value/${cod}/g" ${mer_dat}     ;# Substitui o valor "value" pelo código da localidade 
  sed -i 's/.$//g' ${mer_dat}              ;# retira a última linha do 
  paste ${mer_out} ${mer_dat} > tmp.txt    ;# Junta colunas de dois aquivos em um só
  mv tmp.txt ${mer_out}
  rm -rf ${mer_dat}
  echo $mer_out
  #
  # Gera arquivo das datas TMED SAMET
  #
  cdo -outputtab,value -remapnn,"lon=${lon}_lat=${lat}" $arq_tme  > ${sam_tme}
  sed -i "s/value/${cod}/g" ${sam_tme}     ;# Substitui o valor "value" pelo código da localidade 
  sed -i 's/.$//g' ${sam_tme}              ;# retira a última linha do 
  paste ${tme_out} ${sam_tme} > tmp.txt    ;# Junta colunas de dois aquivos em um só
  mv tmp.txt ${tme_out}
  rm -rf ${sam_tme}
  echo $tme_out
  #
  # Gera arquivo das datas TMIN SAMET
  #
  cdo -outputtab,value -remapnn,"lon=${lon}_lat=${lat}" $arq_tmi  > ${sam_tmi}
  sed -i "s/value/${cod}/g" ${sam_tmi}     ;# Substitui o valor "value" pelo código da localidade 
  sed -i 's/.$//g' ${sam_tmi}              ;# retira a última linha do 
  paste ${tmi_out} ${sam_tmi} > tmp.txt    ;# Junta colunas de dois aquivos em um só
  mv tmp.txt ${tmi_out}
  rm -rf ${sam_tmi}
  echo $tmi_out
  #
  # Gera arquivo das datas TMAX SAMET
  #
  cdo -outputtab,value -remapnn,"lon=${lon}_lat=${lat}" $arq_tma  > ${sam_tma}
  sed -i "s/value/${cod}/g" ${sam_tma}     ;# Substitui o valor "value" pelo código da localidade 
  sed -i 's/.$//g' ${sam_tma}              ;# retira a última linha do 
  paste ${tma_out} ${sam_tma} > tmp.txt    ;# Junta colunas de dois aquivos em um só
  mv tmp.txt ${tma_out}
  rm -rf ${sam_tma}
  echo $tma_out

done
#
########################################################
#  Gera o Arquivo .csv MERGE
########################################################
#
sed -i 's/-9.99e+08/ NaN/g' ${mer_out}    ;# substitui valores indefinidos por NaN 
cp -rf ${mer_out} ${mer_csv}
sed -i 's/#/ /g' ${mer_csv}               ;# Substitui # por espaço
sed -i 's/\t/,/g' ${mer_csv}              ;# Substitui Tabs por ,
sed -i 's/ \+//g' ${mer_csv}              ;# Remove um ou mais espaços
echo " Arquivo Gerado -> " ${mer_csv}

#
########################################################
#  Gera o Arquivo .csv SAMET TMED
########################################################
#
sed -i 's/-9.99e+08/ NaN/g' ${tme_out}    ;# substitui valores indefinidos por NaN 
cp -rf ${tme_out} ${tme_csv}
sed -i 's/#/ /g' ${tme_csv}               ;# Substitui # por espaço
sed -i 's/\t/,/g' ${tme_csv}              ;# Substitui Tabs por ,
sed -i 's/ \+//g' ${tme_csv}              ;# Remove um ou mais espaços
echo " Arquivo Gerado -> " ${tme_csv}

#
########################################################
#  Gera o Arquivo .csv SAMET TMIN
########################################################
#
sed -i 's/-9.99e+08/ NaN/g' ${tmi_out}    ;# substitui valores indefinidos por NaN 
cp -rf ${tmi_out} ${tmi_csv}
sed -i 's/#/ /g' ${tmi_csv}               ;# Substitui # por espaço
sed -i 's/\t/,/g' ${tmi_csv}              ;# Substitui Tabs por ,
sed -i 's/ \+//g' ${tmi_csv}               ;# Remove um ou mais espaços
echo " Arquivo Gerado -> " ${tmi_csv}

#
########################################################
#  Gera o Arquivo .csv SAMET TMAX
########################################################
#
sed -i 's/-9.99e+08/ NaN/g' ${tma_out}    ;# substitui valores indefinidos por NaN 
cp -rf ${tma_out} ${tma_csv}
sed -i 's/#/ /g' ${tma_csv}               ;# Substitui # por espaço
sed -i 's/\t/,/g' ${tma_csv}              ;# Substitui Tabs por ,
sed -i 's/ \+//g' ${tma_csv}              ;# Remove um ou mais espaços
echo " Arquivo Gerado -> " ${tma_csv}

#
#########################################################################
### WRITE FINAL TIME OF SCRIPT EXECUTION                              ###
#########################################################################
#
#echo "Tempo Final: " >> ${arq_time}
#date >> ${arq_time}
#
#########################################################################
### APAGA DADOS TEMPORÁRIOS                                          ###
#########################################################################
#
#rm -rf $path_dat/*.txt $path_dat/*.csv
rm -rf nohup.out


exit
