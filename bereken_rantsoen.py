import numpy as np
import pandas as pd
import scipy as sp
import sys

"""
Dit bestand berekent een economisch optimaal rantsoen voor een koe aan de hand van de door de gebruiker geleverde data.
Het rantsoen wordt berekend op basis van de kosten per kg DS, gelimiteerd door de aangegeven voedingsstoffen en de streefwaarden waaraan het moet voldoen.
Het resultaat zal worden opgeslagen in een Excel-bestand met de naam 'rantsoen_{naam}.xlsx'.

De gebruiker moet de volgende gegevens aanleveren:
- De locatie van een xlsx-bestand waarvan de eerste 5 kolommen de volgende waarden bevatten
    | Categorie | Item | PRIJS [ton DS] | PRIJS [kg DS] | DS [%] | 
  De overige kolommen worden opgevat als lineare beperkingen voor de voedingsstoffen.
  Rij 1 en 4 van het bestand worden genegeerd; Rij 2 bevat de bovenwaarde van de streefwaarde en Rij 3 de onderwaarde van de streefwaarde.
  De overige rijen worden opgevat als de beschikbare voedingsmiddelen.
  'inf' wordt geinterpreteerd als een oneindige waarde, wat betekent dat er geen bovenwaarde van toepassinging is
  
- De naam van het rantsoen, deze wordt gebruikt om het Excel-bestand op te slaan.

Als er geen mogelijk rantsoen gevonden kan worden, zal er een foutmelding worden weergegeven en wordt het Excel-bestand niet aangemaakt.
Anders worden het rantsoen en de bijbehorende prijs opgeslagen in een Excel-bestand met de naam 'rantsoen_{naam}.xlsx'.
"""

def laad_excel(bestandsnaam):
    """
    Laadt de gegevens uit een Excel-bestand en retourneert een DataFrame.
    """
    try:
        df = pd.read_excel(bestandsnaam, header=None)
        if df.shape[1] < 5:
            raise ValueError("Het Excel-bestand moet ten minste 5 kolommen bevatten.")
        return df
    except Exception as e:
        print(f"Fout bij het laden van het Excel-bestand: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Gebruik: python3 bereken_rantsoen.py <bestandsnaam> <naam-rantsoen>")
        sys.exit(1)
    bestandsnaam = sys.argv[1]
    naam_rantsoen = sys.argv[2]
    
    df = laad_excel(bestandsnaam)
    if df.empty:
        print("Het Excel-bestand bevat geen gegevens.")
        sys.exit(1)
