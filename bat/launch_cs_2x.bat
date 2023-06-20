title run_cs_2x
start /W cmd /k Call bat\run_cs_2x.bat & taskkill /IM tanki_2014_debug.exe /f & taskkill /fi "WINDOWTITLE eq run_cs_2x"