## Recorte Espacial e Seleção de Variáveis
#cdo -selname,{variável} == Seleciona a variável do arquivo
#cdo -sellonlatbox,-54,-48.1,-29.5,-25.8 == Recorta SC


#cdo -selname,prec -sellonlatbox,-54,-48.1,-29.5,-25.8 __in__.nc __out__.nc
cdo -selname,tmin -sellonlatbox,-54,-48.1,-29.5,-25.8 SAMeT_CPTEC_DAILY_TMIN_2000_2022.nc samet_tmin_sc.nc
#cdo -selname,tmed -sellonlatbox,-54,-48.1,-29.5,-25.8 SAMeT_CPTEC_DAILY_TMIN_2000_2022.nc samet_tmed_sc.nc
#cdo -selname,tmax -sellonlatbox,-54,-48.1,-29.5,-25.8 __in__.nc samet_tmax_sc.nc
