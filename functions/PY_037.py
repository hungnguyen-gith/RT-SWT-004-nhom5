def update(self, mini_batch, num_sequences):
        """
        Updates model using buffer.
        :param num_sequences: Number of trajectories in batch.
        :param mini_batch: Experience batch.
        :return: Output from update process.
        """
        feed_dict = {self.model.batch_size: num_sequences,
                     self.model.sequence_length: self.sequence_length,
                     self.model.mask_input: mini_batch['masks'].flatten(),
                     self.model.returns_holder: mini_batch['discounted_returns'].flatten(),
                     self.model.old_value: mini_batch['value_estimates'].flatten(),
                     self.model.advantage: mini_batch['advantages'].reshape([-1, 1]),
                     self.model.all_old_log_probs: mini_batch['action_probs'].reshape(
                         [-1, sum(self.model.act_size)])}
        if self.use_continuous_act:
            feed_dict[self.model.output_pre] = mini_batch['actions_pre'].reshape(
                [-1, self.model.act_size[0]])
            feed_dict[self.model.epsilon] = mini_batch['random_normal_epsilon'].reshape(
                [-1, self.model.act_size[0]])
        else:
            feed_dict[self.model.action_holder] = mini_batch['actions'].reshape(
                [-1, len(self.model.act_size)])
            if self.use_recurrent:
                feed_dict[self.model.prev_action] = mini_batch['prev_action'].reshape(
                    [-1, len(self.model.act_size)])
            feed_dict[self.model.action_masks] = mini_batch['action_mask'].reshape(
                [-1, sum(self.brain.vector_action_space_size)])
        if self.use_vec_obs:
            feed_dict[self.model.vector_in] = mini_batch['vector_obs'].reshape(
                [-1, self.vec_obs_size])
            if self.use_curiosity:
                feed_dict[self.model.next_vector_in] = mini_batch['next_vector_in'].reshape(
                    [-1, self.vec_obs_size])
        if self.model.vis_obs_size > 0:
            for i, _ in enumerate(self.model.visual_in):
                _obs = mini_batch['visual_obs%d' % i]
                if self.sequence_length > 1 and self.use_recurrent:
                    (_batch, _seq, _w, _h, _c) = _obs.shape
                    feed_dict[self.model.visual_in[i]] = _obs.reshape([-1, _w, _h, _c])
                else:
                    feed_dict[self.model.visual_in[i]] = _obs
            if self.use_curiosity:
                for i, _ in enumerate(self.model.visual_in):
                    _obs = mini_batch['next_visual_obs%d' % i]
                    if self.sequence_length > 1 and self.use_recurrent:
                        (_batch, _seq, _w, _h, _c) = _obs.shape
                        feed_dict[self.model.next_visual_in[i]] = _obs.reshape([-1, _w, _h, _c])
                    else:
                        feed_dict[self.model.next_visual_in[i]] = _obs
        if self.use_recurrent:
            mem_in = mini_batch['memory'][:, 0, :]
            feed_dict[self.model.memory_in] = mem_in
        self.has_updated = True
        run_out = self._execute_model(feed_dict, self.update_dict)
        return run_out