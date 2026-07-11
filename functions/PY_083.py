def bind(self, data_shapes, label_shapes=None, for_training=True,
             inputs_need_grad=False, force_rebind=False, shared_module=None,
             grad_req='write'):
        """Binds the symbols to construct executors. This is necessary before one
        can perform computation with the module.

        Parameters
        ----------
        data_shapes : list of (str, tuple)
            Typically is ``data_iter.provide_data``.
        label_shapes : list of (str, tuple)
            Typically is ``data_iter.provide_label``.
        for_training : bool
            Default is ``True``. Whether the executors should be bind for training.
        inputs_need_grad : bool
            Default is ``False``. Whether the gradients to the input data need to be computed.
            Typically this is not needed. But this might be needed when implementing composition
            of modules.
        force_rebind : bool
            Default is ``False``. This function does nothing if the executors are already
            bound. But with this ``True``, the executors will be forced to rebind.
        shared_module : Module
            Default is ``None``. This is used in bucketing. When not ``None``, the shared module
            essentially corresponds to a different bucket -- a module with different symbol
            but with the same sets of parameters (e.g. unrolled RNNs with different lengths).
        grad_req : str, list of str, dict of str to str
            Requirement for gradient accumulation. Can be 'write', 'add', or 'null'
            (default to 'write').
            Can be specified globally (str) or for each argument (list, dict).
        """
        if self.binded and not force_rebind:
            self.logger.warning('Already bound, ignoring bind()')
            return

        assert grad_req == 'write', "Python module only support write gradient"
        self.for_training = for_training
        self.inputs_need_grad = inputs_need_grad

        assert len(data_shapes) == len(self._data_names)
        assert [x[0] for x in data_shapes] == self._data_names
        self._data_shapes = data_shapes

        self._label_shapes = label_shapes
        if label_shapes is not None:
            assert self._label_names is not None
            assert len(self._label_names) == len(label_shapes)
            assert [x[0] for x in label_shapes] == self._label_names

        self._output_shapes = self._compute_output_shapes()