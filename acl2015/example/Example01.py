from ..components import KnowledgeMiner, KnowledgeBasedLearner, TargetTask, Test, CloseDomain

dataPath = 'sample_data/abc_1'
close_domain_path = 'sample_data/stat/1523723936697'

km = KnowledgeMiner.KnowledgeMiner(dataPath)

close_domain = CloseDomain.CloseDomain(close_domain_path)
close_domain.read_folder()

# 1 1 0 0 = su dung mien qua khu
# 2 0 1 0 = su dung mien hien tai
# 3 1 1 0 = su dung mien qua khu + hien tai
# 4 1 0 1 = su dung mien gan
# 5 1 1 1 = su dung mien gan + hien tai

# current_task_index = 0
# km.set_current_task(current_task_index)
# km.set_close_kb(close_domain.v_sort[current_task_index], 5)
# target = TargetTask.TargetTask(km.get_current_task(), 5)
# kbl = KnowledgeBasedLearner.KnowledgeBaseLearner(0, 1, 0, target.get_target_task(0), km, 1, 10, 6, 6, 0.1)
# kbl.optimize()

true_pos = 0
true_neg = 0
false_pos = 0
false_neg = 0

for j in range(0, 20):
    current_task_index = j
    km.set_current_task(current_task_index)
    km.set_close_kb(close_domain.v_sort[current_task_index], 5)

    target = TargetTask.TargetTask(km.get_current_task(), 5)

    past = 0
    current = 1
    close = 0

    if current == 0:
        fold = 1
    else:
        fold = 5
    for i in range(0, fold):
        kbl = KnowledgeBasedLearner.KnowledgeBaseLearner(
            past, current, close, target.get_target_task(i), km, 1, 10, 6, 6, 0.1)

        if current == 0:
            docs = target.task.docs
        else:
            docs = target.get_test_data(i)

        test = Test.Test(kbl, docs, target.words)
        test.run_test()

        true_pos += test.true_pos
        true_neg += test.true_neg
        false_pos += test.false_pos
        false_neg += test.false_neg

        print i
        print len(docs)
        print test.true_pos, test.true_neg, test.false_pos, test.false_neg, true_pos + true_neg + false_pos + false_neg
        print '------------------'

print true_pos, true_neg, false_pos, false_neg
p_pos = float(true_pos)/float(true_pos + false_pos)
r_pos = float(true_pos)/float(true_pos + false_neg)
p_neg = float(true_neg)/float(true_neg + false_neg)
r_neg = float(true_neg)/float(true_neg + false_pos)
a = float(true_neg + true_pos)/(true_pos + true_neg + false_pos + false_neg)

print p_pos, r_pos, 2 * p_pos * r_pos / (p_pos + r_pos)
print p_neg, r_neg, 2 * p_neg * r_neg / (p_neg + r_neg)
print a
