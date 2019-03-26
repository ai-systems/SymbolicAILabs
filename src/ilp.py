import sys
import re

from trimlogic.predicate import KnowledgeBase
from trimlogic.predicate import RuleBasedPredicate
from trimlogic.predicate import AtomFactory
from trimlogic.foil import foil
from trimlogic.algorithm import fol_bc_ask
from helper import assertFollows, print_rules, Temperature, Carbon

knowledgeBase = KnowledgeBase()

highTemp = RuleBasedPredicate('HIGH_TEMPERATURE', (Temperature,))
medTemp = RuleBasedPredicate('MEDIUM_TEMPERATURE', (Temperature,))
lowTemp = RuleBasedPredicate('LOW_TEMPERATURE', (Temperature,))
knowledgeBase.add_all([highTemp, medTemp, lowTemp])

highCarbon = RuleBasedPredicate('HIGH_CARBON', (Carbon,))
medCarbon = RuleBasedPredicate('MEDIUM_CARBON', (Carbon,))
lowCarbon = RuleBasedPredicate('LOW_CARBON', (Carbon,))
knowledgeBase.add_all([highCarbon, medCarbon, lowCarbon])

predicate_dict = {
    'HIGH_CARBON': highCarbon,
    'MEDIUM_CARBON': medCarbon,
    'LOW_CARBON': lowCarbon,
    'HIGH_TEMPERATURE': highTemp,
    'MEDIUM_TEMPERATURE': medTemp,
    'LOW_TEMPERATURE': lowTemp,
}


fact_file = '%s/facts.ilp' % sys.argv[1]
fact_file = open(fact_file)

atom_pattern = ('^[a-zA-Z0-9_.-]+\([a-zA-Z0-9_.-]+\)$')

for line in fact_file:
    line = line.strip()
    line = line.replace(' ', '')
    if line == '':
        continue
    if not re.match(atom_pattern, line):
        message = '%s does not adhere to standards. Program allows only to have predicates of arity 1' % line
        raise Exception(message)
    data = line.split('(')
    predicate = data[0]
    var = data[1].split(')')[0]
    if predicate not in predicate_dict:
        message = '%s predicate does not exist' % predicate
        raise Exception(message)

    rule = predicate_dict[predicate]
    if 'CARBON' in predicate_dict:
        map(rule.add_rule, [(Carbon(var),)])
    else:
        map(rule.add_rule, [(Temperature(var),)])


def process_predicates(process_file, new_predicates):
    atom_pattern = ('^[a-zA-Z0-9_.-]+\([a-zA-Z0-9_.-]+,[a-zA-Z0-9_.-]+\)$')
    tuples = []
    for line in process_file:
        line = line.strip()
        line = line.replace(' ', '')
        if line == '':
            continue
        if not re.match(atom_pattern, line):
            message = '%s does not adhere to standards. Program allows only to have predicates of arity 2' % line
            raise Exception(message)
        data = line.split('(')
        predicate = data[0]
        if predicate not in new_predicates:
            rule_pred = RuleBasedPredicate(predicate, (Temperature, Carbon))
            new_predicates[predicate] = rule_pred
        var1, var2 = data[1].split(')')[0].split(',')
        tuples.append([Temperature(var1), Carbon(var2)])

    return new_predicates, tuples


new_predicates = {}

negative_file = '%s/negative.ilp' % sys.argv[1]
negative_file = open(negative_file)
new_prdicates, negative_tuples = process_predicates(
    negative_file, new_predicates)

positive_file = '%s/positive.ilp' % sys.argv[1]
positive_file = open(positive_file)

new_prdicates, positive_tuples = process_predicates(
    positive_file, new_predicates)

for pred in new_predicates.values():
    knowledgeBase.add(pred)
    foil(pred, positive_tuples, negative_tuples, knowledgeBase, ordering=None)
    print_rules(pred)
