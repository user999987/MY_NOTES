```kotlin
// y非空转int y空则认为当前obj是"ri", 当前对象存在在运行 let内函数
// The context object is available as an argument (it). The return value is the lambda result.
// https://kotlinlang.org/docs/scope-functions.html#functions
y?.toInt()?:"ri".let {
        println(it)
    }
```

```kotlin
// configA
@Bean("transientWebClientResponseException")
  fun retryBackoffSpecTransientWebClientResponseException(): RetryBackoffSpec {
    return Retry.backoff(
      retryMaxAttempts.toLong(),
      Duration.ofMillis(minBackoffTimeoutMs.toLong())
    )
      .jitter(jitterFactor.toDouble())
      .transientErrors(true)
      .filter {
        ((it is WebClientResponseException) &&
          (it.statusCode == HttpStatus.REQUEST_TIMEOUT ||
            it.statusCode == HttpStatus.INTERNAL_SERVER_ERROR ||
            it.statusCode == HttpStatus.NOT_IMPLEMENTED ||
            it.statusCode == HttpStatus.BAD_GATEWAY ||
            it.statusCode == HttpStatus.SERVICE_UNAVAILABLE ||
            it.statusCode == HttpStatus.GATEWAY_TIMEOUT)
          )
      }
  }

// configB
  @Autowired
  @Qualifier("transientWebClientResponseException")
  lateinit var retrySpec: RetryBackoffSpec
```

```kotlin
val generatedArray=Array(10){i-> i}
```

```kotlin
if (targetDomainObject is Array<*>) {
      targetDomainObject.first().toString()
    } else {
      targetDomainObject.toString()
    }
```

```kotlin
Flux.fromArray(generatedArray)
```