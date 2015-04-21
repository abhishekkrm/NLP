 
answeryToNerMap = {
        'ABBR:exp'      :[ [],'abbreviation:expression abbreviation' ],
        'ABBR:abb'      :[[],'abbreviation:abbreviation'],

        'ENTY:animal'   :[[],'entities:animals'],
        'ENTY:body'     :[[],'entities:organs of body'],
        'ENTY:color'    :[[],'colors'],
        'ENTY:cremat'   :[[],'entities:inventions, books and other creative pieces'],
        'ENTY:currency' :[[],'entities:currency names'],
        'ENTY:dismed'   :[[],'entities:diseases and medicine'],
        'ENTY:event'    :[[],'entities:events'],
        'ENTY:food'     :[[],'entities:food'],
        'ENTY:instru'   :[[],'entities:musical instrument'],        
        'ENTY:lang'     :[[],'entities:languages'],
        'ENTY:letter'   :[[],'entities:letters like a-z'],
        'ENTY:other'    :[[],'entities:other entities'],
        'ENTY:plant'    :[[],'plants'],
        'ENTY:product'  :[[],'entities:products'],
        'ENTY:religion' :[[],'entities:religions',[[],]],
        'ENTY:sport'    :[[],'sport'],
        'ENTY:substance':[[],'entities:elements and substances'],
        'ENTY:symbol'   :[[],'entities:symbols and signs'],
        'ENTY:techmeth' :[[],'entities:techniques and methods'],
        'ENTY:termeq'   :[[],'entities:equivalent terms'],
        'ENTY:veh'      :[[],'entities:vehicles'],
        'ENTY:word'     :[[],'entities:words with a special property'],
        
        'DESC:def'      :[[],'description:definition'],
        'DESC:desc'     :[[],'description:description'],
        'DESC:manner'   :[[],'description:manner'],
        'DESC:reason'   :[[],'description:reasons'],

        'HUM:gr'        :[['ORGANIZATION','PERSON'],'human beings:a group or organization of persons'],
        'HUM:ind'       :[['ORGANIZATION','PERSON'],'human beings:an individual'],
        'HUM:title'     :[['ORGANIZATION','PERSON'],'human beings:title of a person'],
        'HUM:desc'      :[[],'human beings:description of a person'],
        
        'LOC:city'      :[['LOCATION'],'locations:cities'],
        'LOC:country'   :[['LOCATION'],'locations:countries'],
        'LOC:mount'     :[[],'locations:mountains'],
        'LOC:other'     :[['LOCATION'],'locations:other locations'],
        'LOC:state'     :[['LOCATION'],'locations:states'],
        
        'NUM:code'      :[[],'numeric:postcodes or other codes'],
        'NUM:count'     :[[],'numeric:number'],
        'NUM:date'      :[[],'numeric:dates'],
        'NUM:dist'      :[[],'numeric:linear measures'],
        'NUM:money'     :[[],'numeric:prices'],
        'NUM:ord'       :[[],'numeric:ranks'],
        'NUM:other'     :[[],'numeric:other numbers'],
        'NUM:period'    :[[],'numeric:ranks'],
        'NUM:perc'      :[[],'numeric:percent'],
        'NUM:speed'     :[[],'numeric:speed'],
        'NUM:temp'      :[[],'numeric:temperature'],
        'NUM:volsize'   :[[],'numeric:size, area and volume'],
        'NUM:weight'    :[[],'numeric:weight'],
        }
    
''' Returns List of Possible NER Type 
'''
def AnswerTypeToNerType(answer_type):
    return answeryToNerMap[answer_type.strip()][0]

''' Given answer type, return its description
'''
def AnswerTypeToDescription(answer_type):
    return answeryToNerMap[answer_type.strip()][1]

