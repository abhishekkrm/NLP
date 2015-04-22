 
answeryToNerMap = {
        'ABBR:exp'      :[[],[]],
        'ABBR:abb'      :[[],[]],

        'ENTY:animal'   :[[],['animal']],
        'ENTY:body'     :[[],['organs','body']],
        'ENTY:color'    :[[],['color']],
        'ENTY:cremat'   :[[],['artifact']],
        'ENTY:currency' :[[],['currency']],
        'ENTY:dismed'   :[[],['disease','medicine']],
        'ENTY:event'    :[[],['event']],
        'ENTY:food'     :[[],['food']],
        'ENTY:instru'   :[[],['musical','instrument']],        
        'ENTY:lang'     :[[],['language']],
        'ENTY:letter'   :[[],['alphabet','letters']],
        'ENTY:other'    :[[],['entities']],
        'ENTY:plant'    :[[],['plant']],
        'ENTY:product'  :[[],['products']],
        'ENTY:religion' :[[],['religion']],
        'ENTY:sport'    :[[],['sport','game']],
        'ENTY:substance':[[],['elements','substances']],
        'ENTY:symbol'   :[[],['symbols','signs']],
        'ENTY:techmeth' :[[],['techniques','methods']],
        'ENTY:termeq'   :[[],['term']],
        'ENTY:veh'      :[[],['vehicle']],
        'ENTY:word'     :[[],['words']],
        
        'DESC:def'      :[[],[]],
        'DESC:desc'     :[[],[]],
        'DESC:manner'   :[[],[]],
        'DESC:reason'   :[[],[]],

        'HUM:gr'        :[['ORGANIZATION'],[]],
        'HUM:ind'       :[['PERSON'],[]],
        'HUM:title'     :[[],[]],
        'HUM:desc'      :[[],[]],
        
        'LOC:city'      :[['LOCATION'],[]],
        'LOC:country'   :[['LOCATION'],[]],
        'LOC:mount'     :[['LOCATION'],[]],
        'LOC:other'     :[['LOCATION'],[]],
        'LOC:state'     :[['LOCATION'],[]],
        
        'NUM:code'      :[[],[]],
        'NUM:count'     :[[],[]],
        'NUM:date'      :[['DATE'],[]],
        'NUM:dist'      :[[],[]],
        'NUM:money'     :[['MONEY'],[]],
        'NUM:ord'       :[[],[]],
        'NUM:other'     :[[],[]],
        'NUM:period'    :[['TIME'],[]],
        'NUM:perc'      :[['PERCENT'],[]],
        'NUM:speed'     :[[],[]],
        'NUM:temp'      :[[],[]],
        'NUM:volsize'   :[[],[]],
        'NUM:weight'    :[[],[]],
        }
    
''' Returns List of Possible NER Type 
'''
def AnswerTypeToNerType(answer_type):
    return answeryToNerMap[answer_type.strip()][0]

''' Given answer type, return its description
'''
def AnswerTypeToDescription(answer_type):
    return answeryToNerMap[answer_type.strip()][1]

