import numpy as np


def prepare_data_BFs(self, fps, initial_mol = 0):
        """Method to prepare the BitFeatures of the largest cluster and the rest of the clusters"""
        if self.first_call:
            raise ValueError('The model has not been fitted yet.')
        
        BFs = self._get_BFs()
        big, rest = BFs[0], BFs[1:]

        data = []
        for BF in rest:
            data.append([BF.n_samples_, BF.linear_sum_.astype(np.int64), BF.mol_indices])

        bigs = []
        for mol in big.mol_indices:
            bigs.append([1, fps[mol - initial_mol].astype(np.int64), [mol]])

        return data, bigs