def check_cluster_structure(brc):
    total_mol = 0
    mol_j_vals = []
    for index, node in enumerate(brc._get_leaves()):
        for c in node.subclusters_:
            mol_j = c.mol_indices
            total_mol+=c.n_samples_
            mol_j_vals.append(mol_j)
            assert c.n_samples_ == len(mol_j), f"Fatal! N_j:{c.n_samples_} and len(mol_j):{len(mol_j)} are incompatible."
    print('Check to ensure all N_j values are identical to all len(mol_j) values passed.')


    print('Total number of molecules:', total_mol)

    mol_j_vals = [i for cl in mol_j_vals for i in cl]

    unique = []
    for m in mol_j_vals:
        if m in unique:
            print(f'Fatal! Index {m} is repeating!')
        else:
            msg = 'There are no repeated indices.'
        unique.append(m)
    if msg:
        print(msg)

    print(f'The range of molecular indices is {min(mol_j_vals)} thru {max(mol_j_vals)}')