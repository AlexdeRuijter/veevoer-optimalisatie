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
        if df.shape[0] < 5:
            raise ValueError("Het Excel-bestand moet ten minste 5 rijen bevatten.")
        return df

    except Exception as e:
        print(f"Fout bij het laden van het Excel-bestand: {e}")
        sys.exit(1)

def bereken_rantsoen(df, naam_rantsoen):
    """
    Bereken het economisch optimale rantsoen op basis van de gegeven DataFrame.
    """
    try:
        # Extract relevant data from the DataFrame
        prijzen = df.iloc[4:, 2].astype(float).values  # Prijs per kg DS
        ds_percentages = df.iloc[4:, 4].astype(float).values  # DS percentage
        voerwaardes = df.iloc[4:, 5:].astype(int).values  # Nutriënten

        # Streefwaarden
        streefwaarden_boven = df.iloc[1, 5:].astype(float).values
        streefwaarden_onder = df.iloc[2, 5:].astype(float).values

        # Verander 'inf' naar np.inf voor correcte behandeling
        streefwaarden_boven = np.where(streefwaarden_boven == 'inf', np.inf, streefwaarden_boven)

        # Bereid de lineaire programmering voor
        c = prijzen     # Kosten per kg DS
        A_ub = np.vstack([voerwaardes.T, -voerwaardes.T])
        #A_ub = np.vstack([ -voerwaardes.T])

        b_ub = np.concatenate([streefwaarden_boven, -streefwaarden_onder])
        #b_ub = np.concatenate([-streefwaarden_onder])
        bounds = [(0, None)] * len(prijzen)  # Geen negatieve hoeveelheden

        # Behandel de nan, inf en -inf waarden zodat ze correct worden geïnterpreteerd
        c = np.nan_to_num(c)
        A_ub = np.nan_to_num(A_ub)
        b_ub = np.nan_to_num(b_ub)

        # Los het lineaire programmeringsprobleem op
        from scipy.optimize import linprog
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        if not result.success:
            print("Geen mogelijk rantsoen gevonden. Probeer de streefwaarden of de beschikbare voedingsmiddelen aan te passen.")
            raise ValueError(f"{result.message}")
        
        # Resultaat verwerken
        rantsoen_1kg_DS = result.x
        rantsoen_prijs = round(result.fun,2)
        rantsoen_per_19kg_DS = rantsoen_1kg_DS * 19
        rantsoen_waardes = [round(i,2) for i in (streefwaarden_onder + result.ineqlin.residual[streefwaarden_onder.shape[0]:])]
        rantsoen_kg_normaal = [round(i,2) for i in rantsoen_per_19kg_DS/ds_percentages]
        rantsoen_per_19kg_DS = [round(i, 2) for i in rantsoen_per_19kg_DS]

        # Maak een DataFrame voor het rantsoen
        s1 = pd.DataFrame({
            'Voermiddel': df.iloc[4:, 1].values, 
            'Rantsoen per koe (niet DS) [kg]:' : rantsoen_kg_normaal,
            'Hoeveelheid 19kg totaal [kg DS]': rantsoen_per_19kg_DS,
            'Prijs per ton DS': prijzen
            }).transpose()
     
        s2 = pd.Series({'Totale prijs [EUR/ ton DS]': rantsoen_prijs})

        s3 = pd.DataFrame({
            'Streefwaarde Type:': df.iloc[0, 5:].values,
            'Streefwaarde Boven:': streefwaarden_boven,
            'Rantsoen Waarde': rantsoen_waardes,
            'Streefwaarde Onder:': streefwaarden_onder,
            }).transpose()

        s_empty = pd.Series({'': ''})

        rantsoen_df = pd.concat([s1,s_empty, s2, s_empty, s3], axis=0)
        
        # Sla het resultaat op in een Excel-bestand
        output_bestandsnaam = f'rantsoen_{naam_rantsoen}.xlsx'
        rantsoen_df.to_excel(output_bestandsnaam, index=True, header=False)

        
    except Exception as e:
        print(f"Fout bij het berekenen van het rantsoen: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Gebruik: python3 bereken_rantsoen.py <bestandsnaam> <naam-rantsoen>")
        sys.exit(1)
    bestandsnaam = sys.argv[1]
    naam_rantsoen = sys.argv[2]
    
    df = laad_excel(bestandsnaam)
    bereken_rantsoen(df, naam_rantsoen)
