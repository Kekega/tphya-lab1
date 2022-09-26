import sys


def parse_input(filename):
    with open(filename, "r", encoding="utf-8") as f:
        rules = f.readlines()
    rules = [rule.strip() for rule in rules]
    d = {}
    for rule in rules:
        for elem in rule.split():
            if elem.isupper():
                d[elem] = []
    for rule in rules:
        key, v = rule.split(" -> ")
        v = "".join(v.split())
        d[key].append(v)
    return d

def first_split_classes(dict):
    unified = {}
    eq_classes = {}
    num_classes = 0
    for nont, definition in dict.items():
        raw_rules_list = []
        for elem in definition:
            t = get_raw_rules(dict, elem)
            raw_rules_list.append(t)
        unified[nont] = raw_rules_list
        eq_classes, num_classes = fill_eq_classes(unified, nont, eq_classes, num_classes)
    return eq_classes, unified, num_classes


def get_raw_rules(d, item):
    pattern = ""
    for symbol in item:
        if symbol in d.keys():
            pattern += "_"
        else:
            pattern += symbol
    return pattern


def fill_eq_classes(parent_dict, item, eq_classes, num):
    t = parent_dict[item]
    for nont, pattern in parent_dict.items():
        if nont != item and set(t) == set(pattern):
            eq_classes[item] = eq_classes.get(nont)
            return eq_classes, num
    eq_classes[item] = num
    num += 1
    return eq_classes, num


def replace_nonterms(rule, d, eq_class):
    res = []
    for i in range(0, len(rule)):
        if rule[i] == '_':
            res.append(str(eq_class.get(d[i])))
        else:
            res.append(rule[i])
    return res


def update_eq_classes(patterns, eq_class, d, num, parents_dict):
    add_class = 0
    flag = False
    new_pat_dict = {}
    for nonterm, defi in d.items():
        cur_patterns = []
        for i in range(0, len(defi)):
            cur_patterns.append(replace_nonterms(patterns.get(nonterm)[i], defi[i], eq_class))
        new_pat_dict[nonterm] = cur_patterns
    for nont, _ in eq_class.items():
        dad = parents_dict[eq_class[nont]]
        if dad == nont:
            continue
        if new_pat_dict[dad] != new_pat_dict[nont]:
            flag = True
            # try to get new parent
            t = try_to_find_parent(eq_class, new_pat_dict, nont, eq_class[nont], patterns)
            if t == -1:
                add_class = 1
                eq_class[nont] = num
                parents_dict[num] = nont
            else:
                eq_class[nont] = t
            break
    return flag, eq_class, add_class, parents_dict


def try_to_find_parent(eq_class, new_pat_dict, nont, what_was, patterns):
    for k, v in new_pat_dict.items():
        if nont != k and patterns[nont] == patterns[k] and what_was < eq_class[k]:
            return eq_class[k]
    return -1


def display_classes(eq_classes):
    for value in list(set(eq_classes.values())):
        print([k for k in eq_classes if eq_classes[k] == value])


def display_simple_case(d):
    for nont, definition in d.items():
        for item in definition:
            print(nont + " -> " + " ".join(item))


def display_answer(d, eq_classes, parents):
    for c, dad in parents.items():
        definition = d[dad]
        for rule in definition:
            print(dad + " ->", end='')
            res = ''
            for elem in rule:
                res += ' '
                if elem.islower():
                    res += elem
                else:
                    res += parents[eq_classes[elem]]

            print(res)


def sort_dict(eq_classes):
    sorted_keys = sorted(eq_classes, key=eq_classes.get)
    sorted_classes = {}
    for w in sorted_keys:
        sorted_classes[w] = eq_classes[w]
    return sorted_classes


def get_first_member(eq_classes, i):
    for k, v in eq_classes.items():
        if v == i:
            return k


def main(filename="test1_input.txt", output_filename="output.txt"):
    d = parse_input(filename)
    for v in d.values():
        v.sort(key=lambda x: (len(x), x))
    eq_classes, patterns, classes_amount = first_split_classes(d)
    eq_classes = sort_dict(eq_classes)

    class_daddys = {}
    for i in range(classes_amount):
        class_daddys[i] = get_first_member(eq_classes, i)

    flag = True
    while flag:
        flag, eq_classes, class_added, class_daddys = update_eq_classes(patterns, eq_classes, d, classes_amount,
                                                                         class_daddys)
        eq_classes = sort_dict(eq_classes)
        classes_amount += class_added
    with open(output_filename, 'w', encoding="utf-8") as f:
        sys.stdout = f
        display_classes(eq_classes)
        if len(set(eq_classes.values())) == len(eq_classes.keys()):
            display_simple_case(d)
        else:
            display_answer(d, eq_classes, class_daddys)


main()
