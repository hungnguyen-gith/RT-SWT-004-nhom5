def take(self, num):
        """
        Take the first num elements of the RDD.

        It works by first scanning one partition, and use the results from
        that partition to estimate the number of additional partitions needed
        to satisfy the limit.

        Translated from the Scala implementation in RDD#take().

        .. note:: this method should only be used if the resulting array is expected
            to be small, as all the data is loaded into the driver's memory.

        >>> sc.parallelize([2, 3, 4, 5, 6]).cache().take(2)
        [2, 3]
        >>> sc.parallelize([2, 3, 4, 5, 6]).take(10)
        [2, 3, 4, 5, 6]
        >>> sc.parallelize(range(100), 100).filter(lambda x: x > 90).take(3)
        [91, 92, 93]
        """
        items = []
        totalParts = self.getNumPartitions()
        partsScanned = 0

        while len(items) < num and partsScanned < totalParts:
            # The number of partitions to try in this iteration.
            # It is ok for this number to be greater than totalParts because
            # we actually cap it at totalParts in runJob.
            numPartsToTry = 1
            if partsScanned > 0:
                # If we didn't find any rows after the previous iteration,
                # quadruple and retry.  Otherwise, interpolate the number of
                # partitions we need to try, but overestimate it by 50%.
                # We also cap the estimation in the end.
                if len(items) == 0:
                    numPartsToTry = partsScanned * 4
                else:
                    # the first parameter of max is >=1 whenever partsScanned >= 2
                    numPartsToTry = int(1.5 * num * partsScanned / len(items)) - partsScanned
                    numPartsToTry = min(max(numPartsToTry, 1), partsScanned * 4)

            left = num - len(items)

            def takeUpToNumLeft(iterator):
                iterator = iter(iterator)
                taken = 0
                while taken < left:
                    try:
                        yield next(iterator)
                    except StopIteration:
                        return
                    taken += 1

            p = range(partsScanned, min(partsScanned + numPartsToTry, totalParts))
            res = self.context.runJob(self, takeUpToNumLeft, p)

            items += res
            partsScanned += numPartsToTry

        return items[:num]