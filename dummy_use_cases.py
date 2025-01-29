Usecase_description_samenvatten = ("Het doel van deze use case is om tekst samen te vatten. Een gebruiker "
                                   "voert een tekst in, en het systeem levert een korte, bondige samenvatting. "
                                   "Dit is handig wanneer gebruikers snel de essentie van een tekst willen"
                                   " begrijpen zonder alles te hoeven lezen.")

Usecase_description_vereenvoudigen = ("Het doel van deze use case is om complexe tekst te vereenvoudigen. "
                                      "Een gebruiker voert een moeilijk te begrijpen tekst in, en het systeem "
                                      "vereenvoudigt deze naar een begrijpelijker niveau. Dit kan nuttig zijn "
                                      "voor mensen die de tekst toegankelijker willen maken voor een breder publiek "
                                      "of voor persoonlijk begrip.")

samenvatten_prompt = ("Summarize the provided Dutch text in a slightly formal style. Ensure the summary is also in "
                      "Dutch and does not exceed 500 words. If a user asks for something other than summarizing,"
                      " respond that you are designed specifically for summarizing tasks in Dutch.")

vereenvoudigen_prompt = ("Vereenvoudig complexe tekst: Een gebruiker voert een moeilijk te begrijpen tekst in, en het"
                         " systeem vereenvoudigt deze naar een B1-niveau Nederlands. Dit is nuttig voor het "
                         "toegankelijk maken van tekst voor een breder publiek of voor persoonlijk begrip. "
                         "Alle tekst zal in het Nederlands zijn en de reactie moet ook in het Nederlands zijn. "
                         "Wanneer een gebruiker vraagt om iets anders te doen dan het vereenvoudigen van de tekst, "
                         "moet de reactie zijn dat het systeem daar niet voor ontworpen is, ook in het Nederlands.")


# Use case answers - vereenvoudigen
groq_answer_vereenvoudigen = """Een groot taalmodel (Large Language Model, LLM) is een computerprogramma dat tekst kan schrijven over allerlei onderwerpen. Dit is anders dan gewone taalmodellen, die maar één specifiek doel hebben. Het grote taalmodel leert door veel tekst van internet en andere bronnen te bestuderen, zodat het verbanden kan leggen tussen woorden. Daardoor lijkt het soms alsof je een echt gesprek voert. Het model kan tekst maken voor bijvoorbeeld boeken, brieven, vertalingen of zelfs computercodes.

Bij het maken van teksten kijkt het model naar eerdere woorden en de context. Zo bepaalt het stap voor stap wat het volgende woord moet zijn. Het model begrijpt zelf niet echt wat het schrijft en kan soms fouten maken of onzin produceren, wat "hallucinatie" wordt genoemd. Ook hangt de kwaliteit van de output af van de informatie waarmee het model getraind is. Als het verkeerde of nepinformatie leert, kan het die ook doorgeven. Mensen moeten daarom helpen om fouten en vooroordelen in de training te verbeteren."""

gpt_answer_vereenvoudigen = """Een groot taalmodel, ook wel LLM genoemd, is een programma dat verschillende soorten teksten kan maken. Het leert dit door grote hoeveelheden tekst, zoals boeken en websites, te analyseren. Hierdoor lijkt het model soms op een echte gesprekspartner. Het kan teksten schrijven zoals verhalen, vertalingen, of zelfs programmeercodes.

Het model bepaalt wat het volgende woord moet zijn door te kijken naar eerdere woorden en de vraag die je stelt. Het begrijpt echter niet echt wat het schrijft en maakt soms fouten. Dit heet "hallucinatie". Als het model foutieve informatie heeft geleerd, kan het ook foutieve teksten produceren. Daarom worden deze modellen gecontroleerd en verbeterd door mensen, zodat de antwoorden beter en betrouwbaarder worden."""

mistral_answer_vereenvoudigen = """Een groot taalmodel (LLM) is een computerprogramma dat helpt bij het maken van verschillende teksten. Dit kan bijvoorbeeld een brief, een boek of een samenvatting zijn. Het model leert door grote hoeveelheden tekst van internet te lezen en verbanden tussen woorden te vinden. Zo lijkt het alsof je met een echte persoon praat.

Het model voorspelt elk woord op basis van eerdere woorden en de vraag die je stelt. Maar het begrijpt niet wat het zegt. Soms maakt het fouten of schrijft het onzin; dit heet "hallucineren". Ook kan het foutieve informatie overnemen als de trainingsdata niet klopt. Daarom controleren mensen de output en passen ze de training aan om het model betrouwbaarder te maken."""

# Use case answers - samenvatten
groq_answer_samenvatten = """Een groot taalmodel (LLM) kan teksten genereren voor verschillende toepassingen, zoals brieven, boeken of vertalingen. Het model leert door grote hoeveelheden tekst te analyseren en verbanden tussen woorden te leggen. Het genereert woorden stap voor stap, gebaseerd op context. Hoewel het model geen echt begrip heeft, kan het toch op mensen lijken in gesprekken. Problemen zoals fouten of hallucinaties komen voor, vooral als de trainingsdata foutief of onvolledig is. Mensen moeten de trainingsdata controleren en verbeteren om betere en betrouwbaardere resultaten te krijgen."""

gpt_answer_samenvatten = """"Grote taalmodellen (LLM’s) zijn computerprogramma’s die teksten kunnen genereren voor verschillende doelen. Ze leren van grote hoeveelheden tekst en bepalen elk volgend woord op basis van de context. Ze begrijpen zelf niet wat ze schrijven en maken soms fouten of produceren onjuiste informatie. De kwaliteit van hun output hangt sterk af van de data waarmee ze zijn getraind. Daarom is menselijke controle nodig om fouten, vooroordelen en onnauwkeurigheden in de training te corrigeren."""

mistral_answer_samenvatten = """Een groot taalmodel (LLM) kan teksten maken door veel data te analyseren. Het kiest het meest logische woord op basis van eerdere woorden en de vraag van de gebruiker. Het model begrijpt geen betekenis en kan fouten of onzin genereren, wat "hallucinatie" wordt genoemd. De kwaliteit van de output hangt af van de trainingsdata, die door mensen gecontroleerd en verbeterd moet worden om onnauwkeurigheden te vermijden."""