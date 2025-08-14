# Economisch optimaal voeren
Met dit project proberen wij een economisch optimaal rantsoen te bepalen dat voldoet aan bepaalde streefwaarden. 
Geen rechten kunnen worden ontleend aan het inzien van deze code. Gebruik op eigen risico.

## Installeren
Alle nodige versies van packages kunnen worden gevonden in python3_requirements.txt in de folder install. 
Om te testen of alles werkt kun je in de de code runnen met als inputs `data_example.xlsx` en `test`.

## Gebruik
Om het script te gebruiken moet je ofwel de code importeren en het script runnen door middel van 
```
optimaliseer_rantsoen("<naam van data-xlsx>", "<naam voor resultaat>")
```
ofwel 
```
python3 bereken_rantsoen.py <naam van data-xlsx> <naam voor resultaat>
```

Als de optimalisatie een oplossing heeft dan wordt deze opgeslagen in `rantsoen_<naam voor resultaat>.xlsx`.

