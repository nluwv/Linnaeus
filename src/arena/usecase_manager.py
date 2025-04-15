class UsecaseManager:
    def __init__(self):
        self.current_usecase = None
        self.current_prompt = None

    def get_current_prompt(self):
        return self.current_prompt
        
    def set_usecase(self, value):
        if value == "samenvatten":
            self.current_usecase = "samenvatten"
            self.current_prompt = self._get_samenvatten_prompt()
        elif value == "vereenvoudigen":
            self.current_usecase = "vereenvoudigen"
            self.current_prompt = self._get_vereenvoudigen_prompt()
        else:
            raise ValueError("Invalid use case value")
        return self.current_prompt

    def _get_samenvatten_prompt(self):
        return """Summarize the provided Dutch text in a slightly formal style. Ensure the summary is also in Dutch and does not exceed 500 words. If a user asks for something other than summarizing, respond that you are designed specifically for summarizing tasks in Dutch."""

    def get_samenvatten_description(self):
        return """"Het doel van deze use case is om tekst samen te vatten. Een gebruiker voert een tekst in, en het systeem levert een korte, bondige samenvatting. Dit is handig wanneer gebruikers snel de essentie van een tekst willen begrijpen zonder alles te hoeven lezen."""

    def _get_vereenvoudigen_prompt(self):
        return """Vereenvoudig complexe tekst: Een gebruiker voert een moeilijk te begrijpen tekst in, en het systeem vereenvoudigt deze naar een B1-niveau Nederlands. Dit is nuttig voor het toegankelijk maken van tekst voor een breder publiek of voor persoonlijk begrip. Alle tekst zal in het Nederlands zijn en de reactie moet ook in het Nederlands zijn. Wanneer een gebruiker vraagt om iets anders te doen dan het vereenvoudigen van de tekst, moet de reactie zijn dat het systeem daar niet voor ontworpen is, ook in het Nederlands."""

    def get_vereenvoudigen_description(self):
        return """"Het doel van deze use case is om complexe tekst te vereenvoudigen. Een gebruiker voert een moeilijk te begrijpen tekst in, en het systeem vereenvoudigt deze naar een begrijpelijker niveau. Dit kan nuttig zijn voor mensen die de tekst toegankelijker willen maken voor een breder publiek of voor persoonlijk begrip."""
