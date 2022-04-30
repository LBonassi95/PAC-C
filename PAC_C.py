import data_structures as ds

NUM = 'num'
CONSTRAINTS = 'constraints'
SEPARATOR = '-'
GOT_S = 'got{}s'.format(SEPARATOR)
GOT_SA = 'got{}sa'.format(SEPARATOR)
GOAL = 'goal'
DONE_PHI = 'done{}phi'.format(SEPARATOR)
DONE_PSI = 'done{}psi'.format(SEPARATOR)
REQUEST = 'request'
STAGE = 'STAGE'
GOAL_ACHIEVED = "goal-achieved"
OPTIMIZED = False


class UnificationError(Exception):
    pass


class ActionFormulaError(Exception):
    pass


def get_fresh_monitoring_atom(name, number):
    return ds.Literal('{}{}{}'.format(name, SEPARATOR, number), False)


def get_constraints_to_monitor(C):
    for constr in C:
        if constr.kind != ds.ALWAYS:
            yield constr


def get_monitoring_atom(constr):
    if constr.kind == ds.SOMETIME:
        return GOT_S
    elif constr.kind == ds.SOMETIMEAFTER:
        return GOT_SA
    elif constr.kind == ds.SOMETIMEBEFORE:
        return DONE_PSI
    elif constr.kind == ds.ATMOSTONCE:
        return DONE_PHI
    elif constr.kind == ds.ALWAYSNEXT:
        return REQUEST
    elif constr.kind == ds.PATTERN:
        return STAGE
    else:
        return None


def gen_stage_atoms(atom_type, monitoring_atoms_counter, num_stages):
    return [ds.Literal('{}{}P{}{}{}'.format(atom_type, SEPARATOR, monitoring_atoms_counter, SEPARATOR, i), False) for i in range(num_stages)]


def get_monitoring_atoms(C):
    monitoring_atoms = []
    monitoring_atoms_counter = 0
    for constraint in C:
        if constraint.kind != ds.ALWAYS:
            atom_type = get_monitoring_atom(constraint)
            if constraint.kind == ds.PATTERN:
                stage_atoms = gen_stage_atoms(atom_type, monitoring_atoms_counter, len(constraint.gd1))
                constraint.set_monitoring_atoms([stage_atom.literal for stage_atom in stage_atoms])
                monitoring_atoms += stage_atoms
            else:
                monitoring_atom = get_fresh_monitoring_atom(atom_type, monitoring_atoms_counter)
                monitoring_atoms.append(monitoring_atom)
                constraint.set_monitoring_atom_predicate(monitoring_atom.literal)
            monitoring_atoms_counter += 1
    return monitoring_atoms


def create_cond_eff(condition, eff):
    conditional_effect = (condition, eff)
    return conditional_effect


def add_cond_eff(E, cond_eff):
    cond, eff = cond_eff
    if cond.simplified() != ds.FALSE():
        E.append(ds.Effect(cond, eff))


def get_action_set(action_formula):
    if isinstance(action_formula, ds.Literal):
        assert action_formula.negated == False
        action_formula_set = [action_formula.literal]
    elif isinstance(action_formula, ds.Or):
        action_formula_set = [lit.literal for lit in action_formula.components]
    elif isinstance(action_formula, ds.FALSE):
        return []
    else:
        raise ActionFormulaError("Action Formula Error")
    return action_formula_set


def manage_always_compilation(phi, a):
    action_set = get_action_set(phi)
    if a.name not in action_set:
        a.precondition.append(ds.FALSE())


def manage_amo_compilation(phi, m_atom, a):
    action_set = get_action_set(phi)
    monitoring_atom = ds.Literal(m_atom, False)
    if a.name in action_set:
        a.precondition.append(monitoring_atom.negate())
        a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))


def manage_sb_compilation(phi, psi, m_atom, a):
    action_set_phi = get_action_set(phi)
    action_set_psi = get_action_set(psi)
    monitoring_atom = ds.Literal(m_atom, False)
    if a.name in action_set_phi:
        a.precondition.append(monitoring_atom)
    if a.name in action_set_psi:
        a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))


def manage_sometime_compilation(phi, m_atom, a):
    action_set = get_action_set(phi)
    monitoring_atom = ds.Literal(m_atom, False)
    if a.name in action_set:
        a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))


def manage_sa_compilation(phi, psi, m_atom, a):
    action_set_phi = get_action_set(phi)
    action_set_psi = get_action_set(psi)
    monitoring_atom = ds.Literal(m_atom, False)
    if a.name in action_set_phi and a.name not in action_set_psi:
        a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom.negate()))
    if a.name in action_set_psi:
        a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))


def manage_ax_compilation(phi, psi, m_atom, a):
    action_set_phi = get_action_set(phi)
    action_set_psi = get_action_set(psi)
    monitoring_atom = ds.Literal(m_atom, False)

    if a.name not in action_set_phi and a.name not in action_set_psi:
        a.precondition.append(monitoring_atom.negate())

    if a.name in action_set_phi and a.name not in action_set_psi:
        a.precondition.append(monitoring_atom.negate())
        a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))

    if a.name not in action_set_phi and a.name in action_set_psi:
        a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom.negate()))

    if a.name in action_set_phi and a.name in action_set_psi:
        a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))


def manage_fast_always_compilation(phi, A):
    action_set = set(get_action_set(phi))
    new_actions = []
    for a in A:
        if a.name in action_set:
            new_actions.append(a)
    return new_actions


def manage_fast_amo_compilation(phi, m_atom, A):
    action_set = set(get_action_set(phi))
    monitoring_atom = ds.Literal(m_atom, False)
    for a in A:
        if a.name in action_set:
            a.precondition.append(monitoring_atom.negate())
            a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))


def manage_fast_sb_compilation(phi, psi, m_atom, A):
    action_set_phi = set(get_action_set(phi))
    action_set_psi = set(get_action_set(psi))
    monitoring_atom = ds.Literal(m_atom, False)
    for a in A:
        if a.name in action_set_phi:
            a.precondition.append(monitoring_atom)
        if a.name in action_set_psi:
            a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))


def manage_fast_sometime_compilation(phi, m_atom, A):
    action_set = set(get_action_set(phi))
    monitoring_atom = ds.Literal(m_atom, False)
    for a in A:
        if a.name in action_set:
            a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))


def manage_fast_sa_compilation(phi, psi, m_atom, A):
    action_set_phi = set(get_action_set(phi))
    action_set_psi = set(get_action_set(psi))
    monitoring_atom = ds.Literal(m_atom, False)
    for a in A:
        if a.name in action_set_phi and a.name not in action_set_psi:
            a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom.negate()))
        if a.name in action_set_psi:
            a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))


def manage_fast_ax_compilation(phi, psi, m_atom, A):
    action_set_phi = set(get_action_set(phi))
    action_set_psi = set(get_action_set(psi))
    monitoring_atom = ds.Literal(m_atom, False)
    for a in A:
        if a.name not in action_set_phi and a.name not in action_set_psi:
            a.precondition.append(monitoring_atom.negate())

        if a.name in action_set_phi and a.name not in action_set_psi:
            a.precondition.append(monitoring_atom.negate())
            a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))

        if a.name not in action_set_phi and a.name in action_set_psi:
            a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom.negate()))

        if a.name in action_set_phi and a.name in action_set_psi:
            a.effects.append(ds.Effect(ds.TRUE(), monitoring_atom))


def manage_fast_pattern_compilation(gd1, monitoring_atoms, A):
    action_sets = [set(get_action_set(alpha)) for alpha in gd1]
    for action in A:
        for i in range(len(action_sets)):
            if action.name in action_sets[i]:
                if i == 0:
                    action.effects.append(ds.Effect(ds.TRUE(), ds.Literal(monitoring_atoms[i], False)))
                else:
                    action.effects.append(ds.Effect(ds.Literal(monitoring_atoms[i-1], False), ds.Literal(monitoring_atoms[i], False)))


def get_all_effects(a):
    for effect in a.effects:
        yield effect.effect


def unify_actions(a1, a2):
    assert a1.name == a2.name
    if a1.effects == a2.effects:
        # TODO Test This !!!!
        new_precondition = ds.Or(a1.precondition + a2.precondition).simplified()
        new_precondition = ds.Or(list(set(new_precondition.components)))
        return ds.Action(a1.name, new_precondition, a1.effects)
    else:
        raise UnificationError("ERROR! 2 actions with the same name but different effects!!!")


def build_action_dictionary(A):
    ''' FAST DOWNWARD SPLIT ACTION IF THEY HAVE A DISJUNCTIVE PRECONDITION '''
    action_dict = {}
    for action in A:
        if action_dict.get(action.name) is None:
            action_dict[action.name] = action
        else:
            action_dict[action.name] = unify_actions(action_dict.get(action.name), action)
    return action_dict


def normalize_formula(gd1, A_set):

    if isinstance(gd1, ds.Or):
        for lit in gd1.components:
            if isinstance(lit, ds.Literal):
                if lit.negated:
                    raise ActionFormulaError("Negative literal in disjunction!")
            else:
                raise ActionFormulaError("Non atomic formula in disjunction!")
        return gd1

    elif isinstance(gd1, ds.And):
        action_set = set()
        for lit in gd1.components:
            if isinstance(lit, ds.Literal):
                if lit.negated:
                    action_set.add(lit.literal)
                else:
                    raise ActionFormulaError("Positive literal in conjunction!")
            else:
                raise ActionFormulaError("Non atomic formula in conjunction!")
        positive_set = A_set.difference(action_set)
        return ds.Or([ds.Literal(pos, False) for pos in positive_set])

    elif isinstance(gd1, ds.Literal):
        action_set = set()
        if not gd1.negated:
            return gd1
        else:
            action_set.add(gd1.literal)
            positive_set = A_set.difference(action_set)
            return ds.Or([ds.Literal(pos, False) for pos in positive_set])

    elif isinstance(gd1, ds.TRUE):
        print('Warning! an action formula is always satisfied')
        return ds.Or([ds.Literal(act, False) for act in A_set])
    else:
        return gd1 #When falsity


def normalize_constraints_formulae(C, A):
    A_set = set([a.name for a in A])
    for c in C:
        if ds.isNary(c.kind):
            c.gd1 = [normalize_formula(gd, A_set) for gd in c.gd1]
        elif not ds.has2gd(c.kind):
            c.gd1 = normalize_formula(c.gd1, A_set)
        else:
            c.gd1 = normalize_formula(c.gd1, A_set)
            c.gd2 = normalize_formula(c.gd2, A_set)


def manage_pattern_compilation(gd1, monitoring_atoms, action):
    action_sets = [get_action_set(alpha) for alpha in gd1]
    for i in range(len(action_sets)):
        if action.name in action_sets[i]:
            if i == 0:
                action.effects.append(ds.Effect(ds.TRUE(), ds.Literal(monitoring_atoms[i], False)))
            else:
                action.effects.append(ds.Effect(ds.Literal(monitoring_atoms[i-1], False), ds.Literal(monitoring_atoms[i], False)))


# def pac_c(F, A, I, G, C):
#     normalize_constraints_formulae(C, A)
#     monitoring_atoms = get_monitoring_atoms(C)
#     A_prime = []
#     for action in A:
#         for c in C:
#             if c.kind == ds.ALWAYS:
#                 manage_always_compilation(c.gd1, action)
#             elif c.kind == ds.ATMOSTONCE:
#                 manage_amo_compilation(c.gd1, c.monitoring_atom, action)
#             elif c.kind == ds.SOMETIMEBEFORE:
#                 manage_sb_compilation(c.gd1, c.gd2, c.monitoring_atom, action)
#             elif c.kind == ds.SOMETIME:
#                 manage_sometime_compilation(c.gd1, c.monitoring_atom, action)
#             elif c.kind == ds.SOMETIMEAFTER:
#                 manage_sa_compilation(c.gd1, c.gd2, c.monitoring_atom, action)
#             elif c.kind == ds.ALWAYSNEXT:
#                 manage_ax_compilation(c.gd1, c.gd2, c.monitoring_atom, action)
#             elif c.kind == ds.PATTERN:
#                 manage_pattern_compilation(c.gd1, c.monitoring_atoms, action)

#         if ds.FALSE() not in action.precondition:
#             A_prime.append(action)

#     request_atoms = []
#     got_sometime_atoms = []
#     got_sometime_after_atoms = []
#     stage_atoms_goals = []
#     for c in C:
#         if c.kind == ds.SOMETIME:
#             got_sometime_atoms.append(ds.Literal(c.monitoring_atom, False))
#         elif c.kind == ds.SOMETIMEAFTER:
#             got_sometime_after_atoms.append(ds.Literal(c.monitoring_atom, False))
#         elif c.kind == ds.ALWAYSNEXT:
#             request_atoms.append(ds.Literal(c.monitoring_atom, True))
#         elif c.kind == ds.PATTERN:
#             stage_atoms_goals.append(ds.Literal(c.monitoring_atoms[len(c.monitoring_atoms)-1], False))
#     G_prime = ds.And([G, ds.And(request_atoms), ds.And(got_sometime_atoms), ds.And(got_sometime_after_atoms), ds.And(stage_atoms_goals)]).simplified()
#     return F + monitoring_atoms, A_prime, I + got_sometime_after_atoms, G_prime


def get_all_actions(cond):
    if isinstance(cond, ds.Or):
        return [comp.literal for comp in cond.components]
    elif isinstance(cond, ds.Literal):
        return [cond.literal]
    elif isinstance(cond, ds.FALSE):
        return []
    else:
        assert False


def get_relevant_actions(c, action_dict):
    if c.kind == ds.SOMETIME:
        return [action_dict[a] for a in get_all_actions(c.gd1)]


def fast_pac_c(F, A, I, G, C, verbose=False):
    normalize_constraints_formulae(C, A)
    monitoring_atoms = get_monitoring_atoms(C)
    for c in C:
        if c.kind == ds.ALWAYS:
            A = manage_fast_always_compilation(c.gd1, A)

    for c in C:
        if c.kind == ds.ATMOSTONCE:
            manage_fast_amo_compilation(c.gd1, c.monitoring_atom, A)
        elif c.kind == ds.SOMETIMEBEFORE:
            manage_fast_sb_compilation(c.gd1, c.gd2, c.monitoring_atom, A)
        elif c.kind == ds.SOMETIME:
            manage_fast_sometime_compilation(c.gd1, c.monitoring_atom, A)
        elif c.kind == ds.SOMETIMEAFTER:
            manage_fast_sa_compilation(c.gd1, c.gd2, c.monitoring_atom, A)
        elif c.kind == ds.ALWAYSNEXT:
            manage_fast_ax_compilation(c.gd1, c.gd2, c.monitoring_atom, A)
        elif c.kind == ds.PATTERN:
            manage_fast_pattern_compilation(c.gd1, c.monitoring_atoms, A)
    A_prime = A

    request_atoms = []
    got_sometime_atoms = []
    got_sometime_after_atoms = []
    stage_atoms_goals = []
    for c in C:
        if c.kind == ds.SOMETIME:
            got_sometime_atoms.append(ds.Literal(c.monitoring_atom, False))
        elif c.kind == ds.SOMETIMEAFTER:
            got_sometime_after_atoms.append(ds.Literal(c.monitoring_atom, False))
        elif c.kind == ds.ALWAYSNEXT:
            request_atoms.append(ds.Literal(c.monitoring_atom, True))
        elif c.kind == ds.PATTERN:
            stage_atoms_goals.append(ds.Literal(c.monitoring_atoms[len(c.monitoring_atoms) - 1], False))
    G_prime = ds.And(
        [G, ds.And(request_atoms), ds.And(got_sometime_atoms), ds.And(got_sometime_after_atoms), ds.And(stage_atoms_goals)]).simplified()
    return F + monitoring_atoms, A_prime, I + got_sometime_after_atoms, G_prime
