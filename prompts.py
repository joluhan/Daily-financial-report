"""Prompts module for Financial Report Generator"""

class PromptManager:
    """Manages prompts for financial analysis"""
    
    @staticmethod
    def get_base_prompt():
        """Get the base financial analysis prompt"""
        return """Génère un tableau structuré au format exportable (Excel) contenant le rapport financier quotidien pour les paires suivantes :  
BCOUSD, NATGASUSD, EURUSD, GBPJPY, XAUUSD, XAUEUR, NAS100USD, SPX500USD.
Le tableau doit contenir les colonnes suivantes :  
- **Paire**  
- **Biais Quotidien** (Haussier, Baissier ou Neutre)  
- **Résumé Exécutif** (très concis en une ligne)  
- **Explication Approfondie du Biais** (explication détaillée en plusieurs phrases)
Pour chaque paire :
1. Analyse les **facteurs fondamentaux** :  
   - Données macroéconomiques récentes (inflation, PIB, emploi, etc.)  
   - Politiques monétaires des banques centrales (Fed, BCE, BoJ, etc.)  
   - Tensions géopolitiques, conflits ou décisions politiques majeures  
   - Impact de la force ou faiblesse du Dollar Américain  
   - Tout autre élément influent (stocks, saisonnalité, demande énergétique, etc.)
2. Utilise un **langage clair et professionnel**, facile à comprendre pour un trader qui suit les marchés au quotidien. Toujours faire des recherches sur les actualités du jours pour former le biais.
3. Fournis le tableau au format exportable (fichier Excel), avec une ligne par paire et des explications précises adaptées au trading sur le timeframe H1 entre 8h et 15h heure de Paris.

Retourne UNIQUEMENT un JSON valide avec cette structure exacte :
{
  "data": [
    {
      "Paire": "BCOUSD",
      "Biais_Quotidien": "Haussier/Baissier/Neutre",
      "Resume_Executif": "résumé en une ligne",
      "Explication_Approfondie": "explication détaillée"
    }
  ]
}"""
    
    @staticmethod
    def get_search_enhanced_prompt():
        """Get enhanced prompt with search instructions"""
        base_prompt = PromptManager.get_base_prompt()
        return base_prompt + "\n\nIMPORTANT: Recherche les actualités financières et économiques les plus récentes pour chaque paire avant de formuler ton analyse."
    
    @staticmethod
    def get_system_message():
        """Get system message for chat completion"""
        return "Tu es un analyste financier expert. Réponds UNIQUEMENT avec du JSON valide."
    
    @staticmethod
    def get_enhanced_system_message():
        """Get enhanced system message with search capabilities"""
        return "Tu es un analyste financier expert avec accès aux données de marché actuelles. Utilise tes connaissances les plus récentes pour analyser les marchés. Réponds UNIQUEMENT avec du JSON valide."