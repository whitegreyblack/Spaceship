set args=0
for %%x in (%*) do set /A args+=1
if %args$ == 1 (
	if exist C:\Users\swhang\Documents\Python\%1\ (
		cd .\Documents\Python\%1
		)
		)
rem (CD .\Documents\Python\%1
::if %args% == 1 (
rem CD .\%1)
