import json

def parse(str):
    bols = str[0]
    bols = '[' + bols + ']'
    print bols
    bol = json.loads(bols)
    for bo in bol:
        print bo
        print bo["objectiveId"] + ", " + bo["description"] + ", " + bo["weight"]
        for ec in bo["evaluation_criteria"]:
            print "\t" +  ec["evaluation_criterionId"] + ", " + ec["evaluation_criterion"] + ", " + ec["criterion_percentage"] + ", " + ec["option1_score"] + ", " + ec["option2_score"]

tbos = [u'{"objectiveId":"objective1","description":"this is objective1","weight":"1", "evaluation_criteria":[{"evaluation_criterionId":"1","evaluation_criterion":"criterion 1"}, {"evaluation_criterionId":"2","evaluation_criterion":"criterion 2"},{"evaluation_criterionId":"3","evaluation_criterion":"criterion 3"}]},{"objectiveId":"objective2","description":"this is objective2","weight":"2","evaluation_criteria":[{"evaluation_criterionId":"4","evaluation_criterion":"criterion 4"},{"evaluation_criterionId":"5","evaluation_criterion":"criterion 5"},{"evaluation_criterionId":"6","evaluation_criterion":"criterion 6"}]}']

num_objectives = 3
num_eval_criteria = 4

def createBOS():
    global tbos
    weight = 1
    sbos = ""
    first = True
    for o_idx in range(1,num_objectives):
        oid = "objective " + str(o_idx)
        weight += 1
        if weight > 5:
            weight = 1
        eca = []
        for e_idx in range(1, num_eval_criteria):
            eid = o_idx * 100 + e_idx
            ec = {"evaluation_criterionId": str(eid), "evaluation_criterion": "o " + str(o_idx) + " eval criterion " + str(e_idx)}
            eca.append(ec)
        bo = {"objectiveId": oid, "description": "this is " + oid, "weight" : weight, "evaluation_criteria": eca}
        if first:
            first = False
        else:
            sbos += ","
        sbos += json.dumps(bo)
    print tbos
    print " ******* 1 *********"
    bos  = '[' + sbos + ']'
    print bos
    print " ******* 2 *********"
    return bos

def getArrayOfDict(bos):
    # this is not good
    bot = bos[0]
    # this is even worse
    bot = '[' + bot + ']'
    bol = json.loads(bot)
    return bol

if __name__ == "__main__":
    #str = [u'{"objectiveId":"u","description":"uuuuuu","weight":"1","evaluation_criteria":[{"evaluation_criterionId":"1","evaluation_criterion":"uuadfoadf","criterion_percentage":"1","option1_score":"2","option2_score":"3"}]},{"objectiveId":"m","description":"mmmm","weight":"2","evaluation_criteria":[{"evaluation_criterionId":"2","evaluation_criterion":"madsfadf","criterion_percentage":"4","option1_score":"5","option2_score":"6"}]}']
    #str = [u'{"objectiveId":"sss","description":"ssssss","weight":"1","evaluation_criteria":[{"evaluation_criterionId":"1","evaluation_criterion":"sssdfafasf","criterion_percentage":"1","option1_score":"2","option2_score":"3"}]},{"objectiveId":"pppp","description":"ppppppppp","weight":"2","evaluation_criteria":[{"evaluation_criterionId":"2","evaluation_criterion":"padfadfadf","criterion_percentage":"4","option1_score":"5","option2_score":"6"}]}']
    #str = [u'{"objectiveId": "s", "description": "sdfadfa", "weight": "1", "evaluation_criteria": [ {"evaluation_criterionId": "1", "evaluation_criterion": "sfasd", "criterion_percentage": "1", "option1_score": "2", "option2_score": "3"}]}, {"objectiveId": "p", "description": "padsds", "weight": "2", "evaluation_criteria": [{"evaluation_criterionId": "2",  "evaluation_criterion": "padfdaf", "criterion_percentage": "4", "option1_score": "5", "option2_score": "6"}]}']
    #parse(str)
    bos = createBOS()
    bol = getArrayOfDict(bos)
    print " ******** 5 ******** "
    print bol