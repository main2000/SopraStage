from datetime import datetime
from pprint import pprint
py_accettato = {'data': [{'anno_stagione': '2024 P/E',
           'data_documento': '2023-09-14',
           'data_ordine': '2023-09-26',
           'cliente': '0100070',
           'items': [{'anno_stagione': '20241',
                      'indice_taglia': 2,
                      'modello': '2416481012200',
                      'qta': 1,
                      'sku': '64810142020042',
                      'variante': '004',
                      'variante_comm': '004',
					  'prezzo': 123.5}],
           'natura_movimento': 'reso',  #natura_movimento accetata: RESO o VENDITA
           'numero_bolla': '35001',
           'numero_documento': '23-2401563-35001',
           'serie_bolla': '23-2401563',
           'tot_capi': 1}]
           }


#controllo se all'interno del payload corretto ho come primo livello 'data', al suo interno abbia 'items' e 'natura_movimento'
def controllo_struttura_payload(payload):
    """ la funzione prende in input un payload e controlla se ha la struttura corretta:
    - primo if controllo se il payload è un dizionario se ho il nome della chiave 'data'
    - secondo if controllo se il valore della chiave 'data' è una lista
    - poi una controllo se per ogni elemento della lista ho un dizionario 
    - controllo se all'interno del dizionario ho le chiavi 'items' e 'natura_movimento' + controllo del valore della chiave
    - se tutto ok la struttura è corretta, altrimenti restituisco False
    """
    
    out = {'data': payload,
           'errors': None}
    
    #uau
    
    if not isinstance(payload, dict) or 'data' not in payload:
        """ return "Tipo struttura non valido o chiave 'data' obbligatoria" """
        out['errors'] = "Payload non valido, struttura dati aspettata: dizionario o chiave 'data' obbligatoria"
        return out

   
    if not isinstance(payload['data'], list):
        """ return "Tipo struttura dati non valido, struttura dati aspettata: lista" """
        out['errors'] = "Tipo struttura dati non valido, struttura dati aspettata: lista"
        return out

    for elemento in payload['data']:
        
        if not isinstance(elemento, dict):
            """ return "Tipo struttura non valido, struttura dati aspettata: dizionario" """
            out['errors'] = "Tipo struttura non valido, struttura dati aspettata: dizionario"
            return out

        if 'items' not in elemento or 'natura_movimento' not in elemento:
            """ return "Nome chiave non valido, nomi chiavi accetati: 'items' e 'natura_movimento'" """
            out['errors'] = "Nome chiave non valido, nomi chiavi accetati: 'items' e 'natura_movimento'"
            return out
        
        if elemento['natura_movimento'] not in ('reso', 'vendita'):
            """ return "Valore chiave non valido, accettato: 'natura_movimento' : 'reso' o 'vendita'" """
            out['errors'] = "Valore chiave non valido, accettato: 'natura_movimento' : 'reso' o 'vendita'"
            return out
    """ return "Payload corretto"      """
    out['data'] = payload['data']
    return out

    

#2. Verificare che tutte le chiavi del payload di esempio siano presenti nei dati ricevuti
def controllo_tutte_le_chiavi_del_payload(py_accettato, payload_da_testare):
    
    """ eseguo un controllo del payload da testare
    - sfrutto il set che non ammette duplicati e mi ricavo e unisco le chiavi dalla chiave dal payload di riferimento
    - faccio la stessa cosa all'interno del ciclo controllando se le chiavi del payload da testare sono uguali a quelle del payload accettato
    """
    out = {
        'data': payload_da_testare,
        'errors': None
    }
    
    risultato_controllo = controllo_struttura_payload(payload_da_testare)
    if isinstance(risultato_controllo, dict) and 'errors' in risultato_controllo:
        return risultato_controllo
    """ if controllo_struttura_payload(payload_da_testare) != "Payload corretto":
        return "Payload non valido" """
    
    chiavi_payload_accettato = set(py_accettato['data'][0].keys())
    chiavi_items_accettato = set(py_accettato['data'][0]['items'][0].keys()) 
    chiavi_payload_accettato = chiavi_payload_accettato.union(chiavi_items_accettato) 
    #print(chiavi_payload_accettato)
    
    for elemento in payload_da_testare['data']:
        
        chiavi_test = set(elemento.keys())
        chiavi_items = set(elemento['items'][0].keys()) 
        chiavi_payload_da_testare = chiavi_test.union(chiavi_items)
        if chiavi_payload_accettato != chiavi_payload_da_testare:
            """ return "Tutte le chiavi del payload non corrispondono da quello di riferimento" """
            out['errors'] = "Una delle chiavi del payload non corrisponde a quello di riferimento"
            return out
    
    """ return "Tutte le chiavi del payload corrispondono a quello di riferimento" """
    out['data'] = payload_da_testare['data']
    return out

def controllo_tutte_le_chiavi_del_payloadd(py_accettato, payload_da_testare):
    out = {'data': None, 'errors': None}

    risultato_controllo = controllo_struttura_payload(payload_da_testare)
    if risultato_controllo['errors']:
        return risultato_controllo

    dati_testati = risultato_controllo['data']

    chiavi_payload_accettato = set(py_accettato['data'][0].keys())
    chiavi_items_accettato = set(py_accettato['data'][0]['items'][0].keys())
    chiavi_totali_accettato = chiavi_payload_accettato.union(chiavi_items_accettato)

    for elemento in dati_testati:
        chiavi_elemento = set(elemento.keys())
        chiavi_items = set(elemento['items'][0].keys())
        chiavi_totali_elemento = chiavi_elemento.union(chiavi_items)

        if chiavi_totali_elemento != chiavi_totali_accettato:
            out['errors'] = "Le chiavi del payload da testare non corrispondono a quelle del payload accettato."
            out['data'] = dati_testati
            return out

    out['data'] = dati_testati
    return out

    
#3. Dopo aver verificato che i campi data_documento e data_ordine rispettino il formato YYYY-MM-DD trasformarli nel formato DD-MM-YYYY

def controllo_e_trasformazione_data(payload_da_testare):
    
    out = {
        'data': payload_da_testare,
        'errors': None
    }
    
    risultato_controllo = controllo_tutte_le_chiavi_del_payload(py_accettato, payload_da_testare)
    if isinstance(risultato_controllo, dict) and 'errors' in risultato_controllo:
        return risultato_controllo
    
    """ if (controllo_struttura_payload(payload_da_testare) != "Payload corretto"
        or controllo_tutte_le_chiavi_del_payload(py_accettato, payload_da_testare) != "Tutte le chiavi del payload corrispondono a quello di riferimento"):
        return "Payload non valido" """
    
    nuovo_payload = payload_da_testare.copy()
    
    for elemento in nuovo_payload['data']:
        if 'data_documento' in elemento:
            valore_data_documento = elemento['data_documento']
            
            try:
                data_documento_anno_mese_giorno = datetime.strptime(valore_data_documento, '%Y-%m-%d')
            except ValueError:
                try:
                    data_documento_anno_mese_giorno = datetime.strptime(valore_data_documento, '%d-%m-%Y')
                except ValueError:
                    out['errors'] = "Formato data_documento non valido"
                    return out
                    """ return "Formato data_documento non valido" """
            elemento['data_documento'] = data_documento_anno_mese_giorno.strftime('%d-%m-%Y')
                
        
        if 'data_ordine' in elemento:
            valore_data_ordine = elemento['data_ordine']
            
            try:
                data_ordine_anno_mese_giorno = datetime.strptime(valore_data_ordine, '%Y-%m-%d')
            except ValueError:
                try:
                    data_ordine_anno_mese_giorno = datetime.strptime(valore_data_ordine, '%d-%m-%Y')
                except ValueError:
                    out['errors'] = "Formato data_ordine non valido"
                    return out
                    """ return "Formato data_ordine non valido" """
            elemento['data_ordine'] = data_ordine_anno_mese_giorno.strftime('%d-%m-%Y') 
    
    out['data'] = nuovo_payload     
    return out  
    
    
#4. Verificare che i dati anagrafici del modello (modello, variante, indice_taglia) siano presenti all'interno dell'anagrafica ANAGRAFICA_MODELLI

def controllo_dati_anagrafica(payload_da_testare, anagrafica_modelli, anagrafica_taglie):
    
    """ eseguo un controllo del payload da testare
    - primo for: ciclo sui valori delle chiavi "data"
    - secondo for: ciclo sui valori delle chiavi "items" indicizzandoli così da recuperare quello non corretto, item sono le chiavi per ogni dizionario
    - recupero il valore delle chiavi modello, variante e indice_taglia
    - next mi recupera il valore successivo e faccio un controllo se il modello e variante sono presenti all'interno dell'anagrafica_modelli
    - se non sono presenti aggiungo l'errore alla lista errori, non uso un return se no mi si interrompe al primo errore
    - 
    """
    out = {
        'data': payload_da_testare,
        'errors': None
    }
    
    risultato_controllo = controllo_tutte_le_chiavi_del_payload(py_accettato, payload_da_testare)
    if isinstance(risultato_controllo, dict) and 'errors' in risultato_controllo:
        return risultato_controllo
    
    """ if (controllo_struttura_payload(payload_da_testare) != "Payload corretto"
        or controllo_tutte_le_chiavi_del_payload(py_accettato, payload_da_testare) != "Tutte le chiavi del payload corrispondono a quello di riferimento"):
        return "Payload non valido" """
    
    errori = []

    for elemento in payload_da_testare.get("data", []):
        for i, item in enumerate(elemento.get("items", [])): 
            modello = item.get("modello")
            variante = item.get("variante")
            indice_taglia = item.get("indice_taglia")

            modello_trovato = next((Valore_passato for Valore_passato in anagrafica_modelli
                if Valore_passato["modello"] == modello and Valore_passato["variante"] == variante),
                None
            )

            if not modello_trovato:
                errori.append(f"Item {i}: modello '{modello}' con variante '{variante}' non trovato.")
                continue

            tipo_taglia = modello_trovato.get("tipo_taglia")
            if tipo_taglia not in anagrafica_taglie:
                errori.append(f"Item {i}: tipo_taglia '{tipo_taglia}' non presente in ANAGRAFICA_TAGLIE.")
                continue

            if str(indice_taglia) not in anagrafica_taglie[tipo_taglia]:
                errori.append(f"Item {i}: indice_taglia '{indice_taglia}' non valido per tipo_taglia '{tipo_taglia}'.")

    if errori:
        out['errors'] = errori
        return out
    
    return out

#5. Verificare che la somma delle qta presenti in ogni singolo items corrisponda al tot_capi

def controllo_somma_qta_uguale_totcapi(payload_da_testare):
    
    out = {
        'data': payload_da_testare,
        'errors': None
    }
    
    risultato_controllo = controllo_tutte_le_chiavi_del_payload(py_accettato, payload_da_testare)
    if isinstance(risultato_controllo, dict) and 'errors' in risultato_controllo:
        return risultato_controllo
    
    risultato_anagrafica = controllo_dati_anagrafica(payload_da_testare, ANAGRAFICA_MODELLI, ANAGRAFICA_TAGLIE)
    if isinstance(risultato_anagrafica, dict) and 'errors' in risultato_anagrafica:
        return risultato_anagrafica
    
    """ if (controllo_struttura_payload(payload_da_testare) != "Payload corretto"
        or controllo_tutte_le_chiavi_del_payload(py_accettato, payload_da_testare) != "Tutte le chiavi del payload corrispondono a quello di riferimento"):
        return "Payload non valido" """

    errori= []
    
    for indice, elemento in enumerate(payload_da_testare['data']):
        tot_capi = elemento.get('tot_capi')
        somma_totale = 0
        #print("tot_capi = ", tot_capi)
        for item in elemento.get('items', []):
            qta = item.get('qta' , 0)
            
            somma_totale += qta
            #print("qta", qta)
        #print("somma_totale = ", somma_totale)
        
        if somma_totale != tot_capi:
            errori.append(f"Dizionario in posizione {indice}: somma qta ({somma_totale}) diversa da tot_capi ({tot_capi}).")
            
    if errori:
        out['errors'] = errori
        return out
    return out  
            
#task6: 6. Per ogni riga aggiungi/recupera/trasforma:
""" #task6: 6. Per ogni riga aggiungi/recupera/trasforma:
    - l'informazione del ml (marchio linea); FATTO
    - l'informazione dell'anno_stagione nel formato esteso: 20241 --> 2024 P/E FATTO
    - l'informazione del modello commerciale (mod8 + est) FATTO
    - l'estensione del modello zfill(3) FATTO
    - l'informazione della competenza FATTO
    - l'informazione della taglia descrittiva  FATTO  """         

def riga_aggiungi_recupera_trasforma(payload_da_testare, anagrafica_modelli, anagrafica_taglie):
    
    out = {
        'data': payload_da_testare,
        'errors': None
    }
    
    
    risultato_controllo = controllo_tutte_le_chiavi_del_payload(py_accettato, payload_da_testare)
    if isinstance(risultato_controllo, dict) and 'errors' in risultato_controllo:
        return risultato_controllo
    
    risultato_trasformazione = controllo_e_trasformazione_data(payload_da_testare)
    if isinstance(risultato_trasformazione, dict) and 'errors' in risultato_trasformazione:
        return risultato_trasformazione
    
    risultato_controllo = controllo_tutte_le_chiavi_del_payload(py_accettato, payload_da_testare)
    if isinstance(risultato_controllo, dict) and 'errors' in risultato_controllo:
        return risultato_controllo 
    
    """ if (controllo_struttura_payload(payload_ta_testare) != "Payload corretto"
        or controllo_tutte_le_chiavi_del_payload(py_accettato, payload_ta_testare) != "Tutte le chiavi del payload corrispondono a quello di riferimento"):
        return "Payload non valido" """
    
    errori = []
    nuovo_payload = payload_da_testare.copy()
    
    for elemento in nuovo_payload['data']:
        for item in elemento['items']:
            modello = item['modello']
            variante = item['variante']
            indice_taglia = str(item['indice_taglia'])
            
            # Recupero la taglia corrispondente
            for valori_modell_variante in anagrafica_modelli:
                if valori_modell_variante['modello'] == modello and valori_modell_variante['variante'] == variante:
                    tipo_taglia = valori_modell_variante['tipo_taglia']
                    
                    if tipo_taglia in anagrafica_taglie and indice_taglia in anagrafica_taglie[tipo_taglia]:
                        item['taglia'] = anagrafica_taglie[tipo_taglia][indice_taglia]
                        
                        
                        item['ml'] = valori_modell_variante['ml'] 
                        
                    
                        item['competenza'] = valori_modell_variante['competenza']
                    
                        est = "0".zfill(2)
                        item['est'] = est  
                    
                        item['modello_comm'] = modello[:-2] + item['est'] 
                else:
                    errori.append(f"Modello '{modello}' con variante '{variante}' non trovato in ANAGRAFICA_MODELLI.")
            item['anno_stagione'] = item['anno_stagione'][:4] + " " + ("P/E")

    if errori:
        out['errors'] = errori
        return out
    
    out['data'] = nuovo_payload
    return out

            
#task7 : 7. Per ogni testata aggiungi/recupera/trasforma: - la ragione sociale; - la nazione
def testata_aggiungi_recupera_trasforma(payload_da_testare, anagrafica_conti):
    
    """ 7. Per ogni testata aggiungi/recupera/trasforma:
    - la ragione sociale;
    - la nazione  """
    
    out = {
        'data': payload_da_testare,
        'errors': None
    }
    
    """ if (controllo_struttura_payload(payload_ta_testare) != "Payload corretto"
        or controllo_tutte_le_chiavi_del_payload(py_accettato, payload_ta_testare) != "Tutte le chiavi del payload corrispondono a quello di riferimento"):
        return "Payload non valido" """
        
    
    risultato_controllo = controllo_tutte_le_chiavi_del_payload(py_accettato, payload_da_testare)
    if isinstance(risultato_controllo, dict) and 'errors' in risultato_controllo:
        return risultato_controllo  

    
    risultato_trasformazione = controllo_e_trasformazione_data(payload_da_testare)
    if isinstance(risultato_trasformazione, dict) and 'errors' in risultato_trasformazione:
        return risultato_trasformazione 
    
    risultato_somma = controllo_somma_qta_uguale_totcapi(payload_da_testare, py_accettato)
    if isinstance(risultato_somma, dict) and 'errors' in risultato_somma:
        return risultato_somma  

    
    risultato_etl_riga = riga_aggiungi_recupera_trasforma(payload_da_testare, ANAGRAFICA_MODELLI, ANAGRAFICA_TAGLIE)
    if isinstance(risultato_etl_riga, dict) and 'errors' in risultato_etl_riga:
        return risultato_etl_riga  

    
    nuovo_payload = risultato_etl_riga['data']
    
    for elemento in nuovo_payload['data']:
       
        for anagrafica in anagrafica_conti:
            if elemento['cliente'] == anagrafica['cliente']:
                elemento['ragione_sociale'] = anagrafica['ragione_sociale']
                elemento['nazione'] = anagrafica['nazione']

        
    out['data'] = nuovo_payload
    return out
    

#task8: Nel caso in cui non si verifica ALMENO uno dei punti sopra indicati (dal pt 1 al pt 5) il ws dovrà restituire un messaggio esplicativo del traceback verificatori, 
""" viceversa dovrà restituire il payload dato in input e stampare a video il nuovo payload costruito con le info del punto 6-7. 

La struttura da utilizzare per il ritorno sarà la seguente:

	out = {
		'data': "payload di partenza",
		'errors' : "eventuali errori"
	} """
 


ANAGRAFICA_CONTI = [{'cliente': '1000100017', 'ragione_sociale': 'FORNERO GIANMARIA', 'nazione': 'IT'},
                    {'cliente': '1000100051', 'ragione_sociale': 'MARY FASHION SRL', 'nazione': 'PL'},
                    {'cliente': '1000100044', 'ragione_sociale': 'KORITALIA TRADE & LOGISTICS S.R.L.', 'nazione': 'MA'},
                    {'cliente': '1000100052', 'ragione_sociale': 'SAFILO UK LTD', 'nazione': 'RO'}]


ANAGRAFICA_MODELLI = [{'modello': '2411221091674', 'variante': '005', 'ml': '611', 'competenza': 'CL', 'tipo_taglia': 'smlxl'},
                      {'modello': '2419291074655', 'variante': '002', 'ml': '694', 'competenza': 'CFA', 'tipo_taglia': 'ncapi'},
                      {'modello': '2419481074674', 'variante': '003', 'ml': '694', 'competenza': 'accessori', 'tipo_taglia': 'cappello'},
                      {'modello': '2416231021670', 'variante': '001', 'ml': '661', 'competenza': 'Imax', 'tipo_taglia': 'ncapi'},
                      {'modello': '2411221042600', 'variante': '010', 'ml': '662', 'competenza': 'CL', 'tipo_taglia': 'smlxl'}]


ANAGRAFICA_TAGLIE = {

    'smlxl': {
            '1': 'XS',
            '2': 'S',
            '3': 'M',
            '4': 'L',
            '5': 'XL',
            '6': 'XXL'},

    'ncapi' : {
            '1': '34',
            '2': '36',
            '3': '38',
            '4': '40',
            '5': '42',
            '6': '44',
            '7': '46',
            '8': '48',
            '9': '50',
           '10': '52'},

    'cappello' : {
            '1': '54',
            '2': '55',
            '3': '56',
            '4': '57',
            '5': '58',
            '6': '59',
            '7': '60',
            '8': '61'},
    }

#payload_test: 
payload_1 = {'data': [{'anno_stagione': '2024 P/E',
           'data_documento': '2023-09-14',
           'data_ordine': '2023-09-26',
           'cliente': '1000100051',
           'items': [{'anno_stagione': '20241',
                      'indice_taglia': '2',
                      'modello': '2411221091674',
                      'qta': 5,
                      'sku': '64810142020042',
                      'variante': '005',
                      'variante_comm': '005',
					  'prezzo': 80},
                      {'anno_stagione': '20241',
                      'indice_taglia': '2',
                      'modello': '2419291074655',
                      'qta': 1,
                      'sku': '64810142020042',
                      'variante': '002',
                      'variante_comm': '002',
					  'prezzo': 30},
                      {'anno_stagione': '20241',
                      'indice_taglia': '8',
                      'modello': '2419481074674',
                      'qta': 5,
                      'sku': '64810142020042',
                      'variante': '010',
                      'variante_comm': '010',
					  'prezzo': 15},
                      {'anno_stagione': '20242',
                      'indice_taglia': '10',
                      'modello': '2416231021670',
                      'qta': 10,
                      'sku': '64810142020042',
                      'variante': '001',
                      'variante_comm': '001',
					  'prezzo': 20}],
           'natura_movimento': 'reso',
           'numero_bolla': '35001',
           'numero_documento': '23-2401563-35001',
           'serie_bolla': '23-2401563',
           'tot_capi': 21}]}

payload_2 = {'data': [{'anno_stagione': '2024 P/E',
           'data_documento': '2023-09-14',
           'cliente': '1000100052',
           'items': [{'anno_stagione': '20241',
                      'indice_taglia': '2',
                      'modello': '2416481012200',
                      'qta': 1,
                      'sku': '64810142020042',
                      'variante': '004',
                      'variante_comm': '004',
					  'prezzo': ''}],
           'natura_movimento': 'reso',
           'numero_bolla': '35001',
           'numero_documento': '23-2401563-35001',
           'serie_bolla': '23-2401563',
           'tot_capi': 1}]}


payload_3 = {'data': [{'anno_stagione': '2024 P/E',
           'data_documento': '2023-12-09',
           'data_ordine': '27-09-2023',
           'cliente': '1000100017',
           'items': [{'anno_stagione': '20241',
                      'indice_taglia': '2',
                      'modello': '2416481012200',
                      'qta': 1,
                      'sku': '64810142020042',
                      'variante': '004',
                      'variante_comm': '004',
					  'prezzo': 30}],
           'natura_movimento': 'reso',
           'numero_bolla': '35001',
           'numero_documento': '23-2401563-35001',
           'serie_bolla': '23-2401563',
           'tot_capi': 1}]}

payload4 = {'data': [{'anno_stagione': '2024 P/E',
           'data_documento': '2023-12-09',
           'data_ordine' : '2023-12-09',
           'cliente': '1000100052',
           'items': [{'anno_stagione': '20241',
                      'indice_taglia': '2',
                      'modello': '2411221091674',
                      'qta': 5,
                      'sku': '64810142020042',
                      'variante': '005',
                      'variante_comm': '005',
					  'prezzo': 15}],
           'natura_movimento': 'vendita',
           'numero_bolla': '35001',
           'numero_documento': '23-2401563-35001',
           'serie_bolla': '23-2401563',
           'tot_capi': 5},
           {'anno_stagione': '2024 P/E',
           'data_documento': '2023-12-15',
            'data_ordine' : '2023-12-09',
           'cliente': '1000100052',
           'items': [{'anno_stagione': '20241',
                      'indice_taglia': '2',
                      'modello': '2411221091674',
                      'qta': 1,
                      'sku': '64810142020042',
                      'variante': '005',
                      'variante_comm': '005',
					  'prezzo': 15}],
           'natura_movimento': 'reso',
           'numero_bolla': '35001',
           'numero_documento': '23-2401563-35001',
           'serie_bolla': '23-2401563',
           'tot_capi': 1},
           {'anno_stagione': '2024 P/E',
           'data_documento': '2023-12-09',
           'data_ordine': '2023-11-10',
           'cliente': '1000100044',
           'items': [{'anno_stagione': '20241',
                      'indice_taglia': '2',
                      'modello': '2419291074655',
                      'qta': 1,
                      'sku': '64810142020042',
                      'variante': '004',
                      'variante_comm': '002',
					  'prezzo': 50}],
           'natura_movimento': 'reso',
           'numero_bolla': '35001',
           'numero_documento': '23-2401563-35001',
           'serie_bolla': '23-2401563',
           'tot_capi': 1},
           {'anno_stagione': '2024 P/E',
           'data_documento': '2023-01-09',
           'data_ordine': '2023-02-20',
           'cliente': '1000100052',
           'items': [{'anno_stagione': '20241',
                      'indice_taglia': '2',
                      'modello': '2411221042600',
                      'qta': 3,
                      'sku': '64810142020042',
                      'variante': '010',
                      'variante_comm': '010',
					  'prezzo': 15}],
           'natura_movimento': 'reso',
           'numero_bolla': '35001',
           'numero_documento': '23-2401563-35001',
           'serie_bolla': '23-2401563',
           'tot_capi': 3},
           {'anno_stagione': '2024 P/E',
           'data_documento': '2023-01-09',
           'data_ordine': '2023-02-20',
           'cliente': '1000100052',
           'items': [{'anno_stagione': '20241',
                      'indice_taglia': '2',
                      'modello': '2411221042600',
                      'qta': 1,
                      'sku': '64810142020042',
                      'variante': '005',
                      'variante_comm': '005',
					  'prezzo': 30}],
           'natura_movimento': 'vendita',
           'numero_bolla': '35001',
           'numero_documento': '23-2401563-35001',
           'serie_bolla': '23-2401563',
           'tot_capi': 2}]}
#task1_1: 1. Verificare che il payload ricevuto in input abbia la struttura sopra indicata
from pprint import pprint
""" print("payload_1: ", controllo_struttura_payload(payload_1))
print("payload_2: ", controllo_struttura_payload(payload_2))
print("payload_3: ", controllo_struttura_payload(payload_3))
print("payload_4: ", controllo_struttura_payload(payload4)) """

""" print("payload_1: \n")
pprint(controllo_struttura_payload(payload_1))
print("payload_2: \n")
pprint(controllo_struttura_payload(payload_2))
print("payload_3: \n")
pprint(controllo_struttura_payload(payload_3))
print("payload_4: \n")
pprint(controllo_struttura_payload(payload4)) """
#-------------------------------------------------------------------------------
#task2: 2. Verificare che tutte le chiavi del payload di esempio siano presenti nei dati ricevuti 
""" print("payload_1: \n")
pprint(controllo_tutte_le_chiavi_del_payloadd(py_accettato, payload_1))
print("payload_2: \n")
pprint(controllo_tutte_le_chiavi_del_payloadd(py_accettato, payload_2))
print("payload_3: \n")
pprint(controllo_tutte_le_chiavi_del_payloadd(py_accettato, payload_3))
print("payload_4: \n")
pprint(controllo_tutte_le_chiavi_del_payloadd(py_accettato, payload4)) """

#task3 : 3. Dopo aver verificato che i campi data_documento e data_ordine rispettino il formato YYYY-MM-DD trasformarli nel formato DD-MM-YYYY

""" print("payload 1: ", controllo_e_trasformazione_data(payload_1), "\n")
print("payload 2: ", controllo_e_trasformazione_data(payload_2), "\n")
print("payload 3: ", controllo_e_trasformazione_data(payload_3), "\n")
print("payload 4: ", controllo_e_trasformazione_data(payload4), "\n") """

#task4 : 4. Verificare che i dati anagrafici del modello (modello, variante, indice_taglia) siano presenti all'interno dell'anagrafica ANAGRAFICA_MODELLI

print("payload_1", controllo_dati_anagrafica(payload_1, ANAGRAFICA_MODELLI, ANAGRAFICA_TAGLIE))
print("payload_2", controllo_dati_anagrafica(payload_2, ANAGRAFICA_MODELLI, ANAGRAFICA_TAGLIE))
print("payload_3", controllo_dati_anagrafica(payload_3, ANAGRAFICA_MODELLI, ANAGRAFICA_TAGLIE))
print("payload_4", controllo_dati_anagrafica(payload4, ANAGRAFICA_MODELLI, ANAGRAFICA_TAGLIE))

#task5 : 5. Verificare che la somma delle qta presenti in ogni singolo items corrisponda al tot_capi

""" print("payload_1: ", controllo_somma_qta_uguale_totcapi(payload_1), "\n")
print("payload_2: ", controllo_somma_qta_uguale_totcapi(payload_2), "\n")
print("payload_3: ", controllo_somma_qta_uguale_totcapi(payload_3), "\n")
print("payload_4: ", controllo_somma_qta_uguale_totcapi(payload4), "\n") """

#task6 : 6. Per ogni riga aggiungi/recupera/trasforma:
"""
print("payload_1: ", riga_aggiungi_recupera_trasforma(payload_1, ANAGRAFICA_MODELLI, ANAGRAFICA_TAGLIE), "\n")
print("payload_2: ", riga_aggiungi_recupera_trasforma(payload_2, ANAGRAFICA_MODELLI, ANAGRAFICA_TAGLIE), "\n")
print("payload_3: ", riga_aggiungi_recupera_trasforma(payload_3, ANAGRAFICA_MODELLI, ANAGRAFICA_TAGLIE), "\n")
print("payload_4: ", riga_aggiungi_recupera_trasforma(payload4, ANAGRAFICA_MODELLI, ANAGRAFICA_TAGLIE), "\n") """ 

#task7 : 7. Per ogni testata aggiungi/recupera/trasforma: - la ragione sociale; - la nazione

""" print("payload_1: ", testata_aggiungi_recupera_trasforma(payload_1, ANAGRAFICA_CONTI), "\n")
print("payload_2: ", testata_aggiungi_recupera_trasforma(payload_2, ANAGRAFICA_CONTI), "\n")
print("payload_3: ", testata_aggiungi_recupera_trasforma(payload_3, ANAGRAFICA_CONTI), "\n")
print("payload_4: ", testata_aggiungi_recupera_trasforma(payload4, ANAGRAFICA_CONTI), "\n")
 """
