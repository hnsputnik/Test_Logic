import NeuroNetLibrary


if __name__ == '__main__':

    nn = NeuroNetLibrary.NeuroNetLibrary()
    nv = NeuroNetLibrary.NeuroVoiceLibrary()

def get_record():

    with nv.listen(entities=entity_list(), recognition_timeout=60000) as r:
        nn.log(r)
    return r

def entity_list():
    
    entity_list = ['confirm', 'wrong_time', 'repeat', 'recommendation_score', 'recommendation', 'question']
    return entity_list

def hello_null():

    if nn.counter('hello_null', '+') >= 2:
        nn.log('event', 'hello_null=1')
        return hangup_null()
    nn.log('unit', 'hello_null')
    r = get_record()
    nv.say('hello_null')
    return hello_logic(r)

def hello_repeat():

    nn.log('unit', 'hello_repeat')
    nv.say('hello_repeat')
    return recommend_main()

def hello():

    nn.log('unit', 'hello_main')
    nv.say('hello_main')
    return hello_logic(r)

### HELLO_LOGIC

def hello_logic(r):

    nn.log('logic', 'hello_logic')

    if not r:
        nn.log ('condition', 'NULL')
        return hello_null()

    if r.entity('confirm') == 'true':
        nn.log('condition','confirm=true')
        return recommend_main()

    if r.entity('confirm') == 'false':
        nn.log('condition','confirm=false')
        return hangup_wrong_time()

    if r.entity('wrong_time') == 'true':
        nn.log('condition','wrong_time=true')
        return hangup_wrong_time()
    
    if r.entity('repeat') == 'true':
        nn.log('condition','repeat=true')
        return hello_repeat()

### MAIN_LOGIC

def main_logic(r):

    nn.log('logic', 'main_logic')

    if not r:
        nn.log('condition', 'NULL')
        return recommend_null()
    
    if r.entity('recommendation_score') in [0,1,2,3,4,5,6,7,8]:
        nn.log('condition','recommendation_score')
        return hangup_negative()

    if r.entity('recommendation_score') in [9,10]:
        nn.log('condition','recommendation_score')
        return hangup_positive()
    
    if r.entity('recommendation') == 'negative':
        nn.log('condition','recommendation=negative')
        return recommend_score_negative()

    if r.entity('recommendation') == 'neutral':
        nn.log('condition','recommendation=neutral')
        return recommend_score_neutral()

    if r.entity('recommendation') == 'positive':
        nn.log('condition','recommendation=positive')
        return recommend_score_positive()

    if r.entity('repeat') == 'true':
        nn.log('condition','repeat=true')
        return recommend_repeat()

    if r.entity('recommendation') == 'dont know':
        nn.log('condition','recommendation=dont know')
        return recommend_repeat_2()
    
    if r.entity('wrong_time') == 'true':
        nn.log('condition','wrong_time=true')
        return hangup_wrong_time()

    if r.entity('question') == 'true':
        nn.log('condition','question=true')
        return forward()

    nn.log('condition', 'DEFAULT')
    return recommend_default()

def recommend_null():

    if nn.counter('recommend_null', '+') >= 2:
        nn.log('event', 'recommend_null=1')
        return hangup_null()
    r = get_record()
    nn.log('goto', 'hello_null')
    nv.say('hello_null')
    return main_logic(r)

def recommend_default():

    if nn.counter('recommend_default', '+') >= 2:
        nn.log('event', 'recommend_default=1')
        return hangup_null()
    r = get_record()
    nn.log('goto', 'recommend_default')
    nv.say('recommend_default')
    return main_logic(r)

### HANGUP_LOGIC

def hangup_positive():
    
    nn.log('tag', 'High score')
    nv.say('hangup_positive')
    nv.hangup()

def hangup_negative():
    nn.log('tag', 'Low score')
    nv.say('hangup_negative')
    nv.hangup()

def hangup_wrong_time():
    nn.log('tag', 'No time to talk')
    nv.say('hangup_wrong_time')
    nv.hangup()

def hangup_null():
    nn.log('tag', 'problems with understanding')
    nv.say('hangup_null')
    nv.hangup()

### FORDWARD_LOGIC

def forward():
    nn.log('goto', 'bridge action')
    nv.say('forward')
    nv.bridge('number')
