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
groq_answer_vereenvoudigen = """Het is moeilijk om de economie duurzamer te maken zonder dat bedrijven daar last van hebben. \
Internationale afspraken zoals het Klimaatakkoord geven richtlijnen, maar veel bedrijven zijn terughoudend. Ze willen hun \
winst op korte termijn beschermen, terwijl er op lange termijn actie nodig is om klimaatverandering tegen te gaan. Ook \
burgers willen duurzaamheid, maar ze vinden de hogere kosten vaak een probleem.\\

Nieuwe technologieën zijn belangrijk om de economie duurzamer te maken. Denk aan groene waterstof of batterijen die energie \
opslaan. Maar deze technologieën zijn nog duur door hoge kosten en weinig mogelijkheden om ze grootschalig te gebruiken. \
Overheden, bedrijven en onderzoekers moeten samenwerken om dit te verbeteren en een balans te vinden tussen economie en het \
klimaat."""

gpt_answer_vereenvoudigen = """Het is lastig om economie en duurzaamheid samen te laten werken. Hoewel het Klimaatakkoord helpt, \
zijn veel bedrijven en burgers huiverig. Bedrijven denken vooral aan hun winst, terwijl er op lange termijn iets moet worden \
gedaan aan klimaatverandering. Burgers willen ook verduurzaming, maar niet als het veel meer geld kost.\\

Nieuwe technologieën zoals waterstof en batterijen kunnen helpen. Toch worden ze nog niet veel gebruikt omdat ze duur zijn en \
er weinig infrastructuur is. Samenwerking tussen de overheid, bedrijven en onderzoekers is nodig om deze problemen op te lossen. \
Zo kunnen we zorgen voor een betere balans tussen geld verdienen en het milieu beschermen."""

mistral_answer_vereenvoudigen = """Het combineren van een sterke economie met zorg voor het klimaat is lastig. Afspraken zoals \
het Klimaatakkoord helpen, maar bedrijven denken vaak eerst aan hun eigen winst. Ook burgers willen dat er iets aan het klimaat \
wordt gedaan, maar ze vinden het moeilijk als dat meer geld kost.\\

Technologie kan een oplossing bieden, zoals waterstof of betere batterijen om energie op te slaan. Maar deze oplossingen zijn nu \
nog duur en moeilijk op grote schaal te gebruiken. Om dit te verbeteren, moeten de overheid, bedrijven en wetenschappers \
samenwerken. Alleen zo kunnen we economie en duurzaamheid in balans brengen."""

# Use case answers - samenvatten
groq_answer_samenvatten = """In mijn stad zijn veel veranderingen, zoals nieuwe gebouwen en meer groen. Mensen vinden het fijn om \
in een groene stad te wonen, maar de huurprijzen zijn wel gestegen, wat het moeilijk maakt voor sommige bewoners om te blijven. De \
gemeente probeert betaalbare woningen te bouwen, maar dit duurt nog wel even.\\

Sommige mensen vinden de veranderingen te snel gaan en vinden dat de oude sfeer verloren gaat. Toch gelooft de gemeente dat deze \
verbeteringen uiteindelijk goed zijn voor iedereen."""

gpt_answer_samenvatten = """"De stad heeft veel nieuwe gebouwen en meer parken gekregen, maar daardoor zijn de huurprijzen gestegen. \
Dit maakt het lastig voor sommige mensen om daar te blijven wonen. De gemeente bouwt nu betaalbare huizen om dit probleem op te lossen, \
maar het kost tijd.\\

Niet iedereen is blij met de veranderingen. Sommige mensen vinden dat de oude sfeer verloren gaat, maar de gemeente blijft proberen \
de stad beter te maken voor iedereen."""

mistral_answer_samenvatten = """In de stad waar ik woon, zijn er veel veranderingen: nieuwe gebouwen en meer groen, wat de stad \
gezelliger maakt. Maar de huurprijzen zijn ook gestegen, wat voor sommige mensen een probleem is. De gemeente werkt aan betaalbare \
woningen om dit op te lossen, maar het duurt lang.\\

Veel mensen vinden dat de stad te snel verandert, en dat de sfeer van de oude wijken verloren gaat. Toch blijft de gemeente doorgaan \
met de verbeteringen, omdat ze denken dat dit uiteindelijk goed is voor iedereen."""