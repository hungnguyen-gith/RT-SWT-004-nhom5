def trigger(self, processingTime=None, once=None, continuous=None):
        """Set the trigger for the stream query. If this is not set it will run the query as fast
        as possible, which is equivalent to setting the trigger to ``processingTime='0 seconds'``.

        .. note:: Evolving.

        :param processingTime: a processing time interval as a string, e.g. '5 seconds', '1 minute'.
                               Set a trigger that runs a query periodically based on the processing
                               time. Only one trigger can be set.
        :param once: if set to True, set a trigger that processes only one batch of data in a
                     streaming query then terminates the query. Only one trigger can be set.

        >>> # trigger the query for execution every 5 seconds
        >>> writer = sdf.writeStream.trigger(processingTime='5 seconds')
        >>> # trigger the query for just once batch of data
        >>> writer = sdf.writeStream.trigger(once=True)
        >>> # trigger the query for execution every 5 seconds
        >>> writer = sdf.writeStream.trigger(continuous='5 seconds')
        """
        params = [processingTime, once, continuous]

        if params.count(None) == 3:
            raise ValueError('No trigger provided')
        elif params.count(None) < 2:
            raise ValueError('Multiple triggers not allowed.')

        jTrigger = None
        if processingTime is not None:
            if type(processingTime) != str or len(processingTime.strip()) == 0:
                raise ValueError('Value for processingTime must be a non empty string. Got: %s' %
                                 processingTime)
            interval = processingTime.strip()
            jTrigger = self._spark._sc._jvm.org.apache.spark.sql.streaming.Trigger.ProcessingTime(
                interval)

        elif once is not None:
            if once is not True:
                raise ValueError('Value for once must be True. Got: %s' % once)
            jTrigger = self._spark._sc._jvm.org.apache.spark.sql.streaming.Trigger.Once()

        else:
            if type(continuous) != str or len(continuous.strip()) == 0:
                raise ValueError('Value for continuous must be a non empty string. Got: %s' %
                                 continuous)
            interval = continuous.strip()
            jTrigger = self._spark._sc._jvm.org.apache.spark.sql.streaming.Trigger.Continuous(
                interval)

        self._jwrite = self._jwrite.trigger(jTrigger)
        return self