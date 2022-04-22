import os
from os import path
import click
import time
from downwardActionConstraints.FDgrounder import ground
import writer
import PAC_C
from converter import convert, get_all_atoms

PLAN_CONSTRAINTS_ = 'Plan constraints:'

ATOMS_OVERHEAD_ = '[ATOMS-OVERHEAD]: {}'

EFFECT_OVERHEAD_ = '[EFFECT-OVERHEAD]: {}'

PRECONDITION_OVERHEAD_ = '[PRECONDITION-OVERHEAD]: {}'

PAC_C_RUNTIME_ = "PAC_C-RUNTIME: {}"

STARTING_PAC_C = "Starting PAC_C"


def print_compilation_overhead(F, F_prime, A_prime):
    print('##### COMPILATION OVERHEAD #####')
    new_atoms = [atom for atom in F_prime if atom not in F]
    preconditions_overhead = 0
    effects_overhead = 0
    atoms_overhead = len(new_atoms)
    for a in A_prime:
        pre_atoms = []
        eff_atoms = []
        for pre in a.precondition:
            atoms_tmp = get_all_atoms(pre)
            for atom in atoms_tmp:
                if atom not in pre_atoms:
                    pre_atoms.append(atom)
        for eff in a.effects:
            eff_atoms.append(eff.effect)
        for lit in eff_atoms:
            if lit in new_atoms or lit.negate() in new_atoms:
                effects_overhead += 1
        for lit in pre_atoms:
            if lit in new_atoms or lit.negate() in new_atoms:
                preconditions_overhead += 1
    print(PRECONDITION_OVERHEAD_.format(preconditions_overhead))
    print(EFFECT_OVERHEAD_.format(effects_overhead))
    print(ATOMS_OVERHEAD_.format(atoms_overhead))


@click.command()
@click.argument('domain')
@click.argument('problem')
@click.argument('output')
@click.option('--verbose', is_flag=True)
@click.option('--show-overhead', is_flag=True)
def main(domain, problem, output, verbose, show_overhead):
    F, A, I, G, C = ground(domain, problem)
    F, A, I, G, C = convert(F, A, I, G, C)
    if verbose:
        print(PLAN_CONSTRAINTS_)
        for c in C:
            print('\t'+str(c)+'\n')
    start_time = time.time()
    print(STARTING_PAC_C)
    F_prime, A_prime, I_prime, G_prime = PAC_C.fast_pac_c(F, A, I, G, C)
    print(PAC_C_RUNTIME_.format(time.time() - start_time))
    if show_overhead:
        print_compilation_overhead(F, F_prime, A_prime)
    output_filename = 'compiled'
    if not path.isdir(output):
        os.system('mkdir {}'.format(output))
    writer.output_compiled_problem(F_prime, A_prime, I_prime, G_prime, output, output_filename)


if __name__ == '__main__':
    main()