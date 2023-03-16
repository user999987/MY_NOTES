WebClient is an interface representing the main entry point for performing web requests.

The interface has a single implementation, the DefaultWebClient class, which we'll be working with.
```kotlin
// Three options to create a WebClient Instance
//1.
WebClient client = WebClient.create();
// static WebClient create() {
//		return new DefaultWebClientBuilder().build();
//	}

//2.
WebClient client = WebClient.create("http://localhost:8080");
//static WebClient create(String baseUrl) {
//		return new DefaultWebClientBuilder().baseUrl(baseUrl).build();
//	}
//3.
WebClient client = WebClient.builder()
  .baseUrl("http://localhost:8080")
  .defaultCookie("cookieKey", "cookieValue")
  .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE) 
  .defaultUriVariables(Collections.singletonMap("url", "http://localhost:8080"))
  .build();
//static WebClient.Builder builder() {
//		return new DefaultWebClientBuilder();
//	}
```
## WebTestClient

```kotlin
WebTestClient
  .bindToServer()
    .baseUrl("http://localhost:8080")
    .build()
    .post()
    .uri("/resource")
  .exchange()
    .expectStatus().is2xxSuccessful.
    .expectStatus().isCreated()
    .expectHeader().valueEquals("Content-Type", "application/json")
    .expectBody().jsonPath("field").isEqualTo("value");
```