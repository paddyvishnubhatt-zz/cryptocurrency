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
            print "\t" +  ec["evaluation_criteriaId"] + ", " + ec["evaluation_criterion"] + ", " + ec["criterion_percentage"] + ", " + ec["option1_score"] + ", " + ec["option2_score"]


if __name__ == "__main__":
    #str = [u'{"objectiveId":"u","description":"uuuuuu","weight":"1","evaluation_criteria":[{"evaluation_criteriaId":"1","evaluation_criterion":"uuadfoadf","criterion_percentage":"1","option1_score":"2","option2_score":"3"}]},{"objectiveId":"m","description":"mmmm","weight":"2","evaluation_criteria":[{"evaluation_criteriaId":"2","evaluation_criterion":"madsfadf","criterion_percentage":"4","option1_score":"5","option2_score":"6"}]}']
    #str = [u'{"objectiveId":"sss","description":"ssssss","weight":"1","evaluation_criteria":[{"evaluation_criteriaId":"1","evaluation_criterion":"sssdfafasf","criterion_percentage":"1","option1_score":"2","option2_score":"3"}]},{"objectiveId":"pppp","description":"ppppppppp","weight":"2","evaluation_criteria":[{"evaluation_criteriaId":"2","evaluation_criterion":"padfadfadf","criterion_percentage":"4","option1_score":"5","option2_score":"6"}]}']
    str = [u'{"objectiveId": "s", "description": "sdfadfa", "weight": "1", "evaluation_criteria": [ {"evaluation_criteriaId": "1", "evaluation_criterion": "sfasd", "criterion_percentage": "1", "option1_score": "2", "option2_score": "3"}]}, {"objectiveId": "p", "description": "padsds", "weight": "2", "evaluation_criteria": [{"evaluation_criteriaId": "2",  "evaluation_criterion": "padfdaf", "criterion_percentage": "4", "option1_score": "5", "option2_score": "6"}]}']
    parse(str)
