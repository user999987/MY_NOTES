## ***Introduction***
Two types of shared variables: *accumulators* to aggregate information and *broadcast varibales* to efficiently distribute large values.

When we normally pass functions to Spark, such as a map() function or a condition for filter(), they can use variables defined outside them in the driver program, but each task running on the cluster gets a new copy of each variable, and updates from these copies are not propagated back to the driver. Spark’s shared variables, accumu‐ lators and broadcast variables, relax this restriction for two common types of com‐ munication patterns: aggregation of results and broadcasts.

## ***Accumulators***
Data Sample as below
```
{"address":"address here", "band":"40m","callsign":"KK6JLK","city":"SUNNYVALE", "contactlat":"37.384733","contactlong":"-122.032164",
"county":"Santa Clara","dxcc":"291","fullname":"MATTHEW McPherrin", "id":57779,"mode":"FM","mylat":"37.751952821","mylong":"-122.4208688735",...}
```
We are loading a list of all of the call signs for which we want to retrieve logs from a file, but we are also interested in how many lines of the input file were blank
```
file = sc.textFile(inputFile)
# Create Accumulator[Int] initialized to 0 
blankLines = sc.accumulator(0)
def extractCallSigns(line):
    global blankLines # Make the global variable accessible 
    if (line == ""):
        blankLines += 1 
    return line.split(" ")
callSigns = file.flatMap(extractCallSigns)
callSigns.saveAsTextFile(outputDir + "/callsigns") 
print "Blank lines: %d" % blankLines.value
```

Note that we will see the right count only after we run the saveAsTextFile() action, because the transformation above it, map(), is lazy, so the side-effect incrementing of the accumulator will happen only when the lazy map() transformation is forced to occur by the saveAsTextFile() action.

Attention!
1. Worker cannot access accumulator. It is a write-only variable.
2. if we want a reliable absolute value counter, regardless of failures or multiple evalua‐ tions, we must put it inside an action like foreach().
    * An accumulator update within a transformation can occur more than once.
    * Spark automatically deals with failed or slow machines by re-executing failed or slow tasks 
    ```
    For example, if the node running a partition of a map() operation crashes, Spark will rerun it on another node; and even if the node does not crash but is simply much slower than other nodes, Spark can preemptively launch a “speculative” copy of the task on another node, and take its result if that finishes. Even if no nodes fail, Spark may have to rerun a task to rebuild a cached value that falls out of memory. The net result is therefore that the same function may run multiple times on the same data depending on what happens on the cluster.
    ```

### ***Custom Accumulator***

accumulator(value, accum_param=None)
    Create an ***Accumulator*** with the given initial value, using a given ***AccumulatorParam*** helper object to define how to add values of the data type if provided. Default AccumulatorParams are used for integers and floating-point numbers if you do not provide one. For other types, a custom AccumulatorParam can be used.

```
>>> from pyspark.accumulators import AccumulatorParam
>>> class VectorAccumulatorParam(AccumulatorParam):
...     def zero(self, value):
...         return [0.0] * len(value)
...     def addInPlace(self, val1, val2):
...         for i in xrange(len(val1)):
...              val1[i] += val2[i]
...         return val1
>>> va = sc.accumulator([1.0, 2.0, 3.0], VectorAccumulatorParam())
```


## ***Broadcast***
Broadcast variables, allows the program to efficiently send a large, read-only value to all the worker nodes for use in one or more Spark operations

Acccumulator sends value to each task, Broadcast sends value to each executor.

```
# Look up the locations of the call signs on the 
# RDD contactCounts. We load a list of call sign 
# prefixes to country code to support this lookup. 

signPrefixes = sc.broadcast(loadCallSignTable())

def processSignCount(sign_count, signPrefixes):
    country = lookupCountry(sign_count[0], signPrefixes.value) 
    count = sign_count[1]
    return (country, count)

countryContactCounts = (contactCounts .map(processSignCount).reduceByKey((lambda x, y: x+ y))) 
countryContactCounts.saveAsTextFile(outputDir + "/countries.txt")
```
We can access this value by calling value on the Broadcast object in our tasks. The value is sent to each node only once, using an efficient, BitTorrent-like communication mechanism.