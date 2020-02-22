# Orbital Game Jam – API
Base URL and port: `http://34.65.4.90:3000`

## Descriptions
### Sentiment classifier
Returns the sentiment of a sentence.

* **URL & Method**
```http
POST /get_sentiment
```
  
*  **Params**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `sentence` | `string` | **Required**. The sentence you want to classify. |

* **Success Response:**

**Code:** 200 <br />
**Content:** `{ sentiment : ["strongly_negative", "negative", "neutral", "positive", "strongly_positive"] }`

### Toxicity classifier
Returns the toxicity class of a sentence.

* **URL & Method**
```http
POST /get_toxicity
```
  
*  **Params**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `sentence` | `string` | **Required**. The sentence you want to classify. |

* **Success Response:**

**Code:** 200 <br />
**Content:** `{ toxicity : ["non-toxic", "toxic", "obscene", "insult", "identity_hate"] }`


### Book information retrieval
Returns the sentence most likely sentence in predefined books, from a list of keywords.

* **URL & Method**
```http
POST /get_information
```
  
*  **Params**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `request` | `string` | **Required**. The list of keywords you are looking for separated by spaces, e.g. "wood dragon gold". |
| `book` | `string` | **Required**. The name of a book you want to look into, can be an of `the_hobbit`, `the_great_gatsby`, `dune`, `1984` or `moby_dick`. |

* **Success Response:**

**Code:** 200 <br />
**Content:** `{ sentence : "Retrieved sentence from the book!" }`

## Sample Calls:
_Warning: These sample calls may not be 100% accurate, the goal is rather to give you an idea about how to use the API in different languages._

### Javascript – Sentiment classifier
```javascript
fetch('http://34.65.4.90:3000/get_sentiment', {
    method: 'POST',
    body: JSON.stringify({ sentence: 'I love Donald Trump.' })
})
.then(console.log)
.catch(console.err)
```

### Java – Toxicity classifier
```java
HttpClient httpclient = HttpClients.createDefault();
HttpPost httppost = new HttpPost("http://34.65.4.90:3000/get_toxicity");

// Request parameters and other properties.
List<NameValuePair> params = new ArrayList<NameValuePair>(1);
params.add(new BasicNameValuePair("sentence", "Am I toxic?"));
httppost.setEntity(new UrlEncodedFormEntity(params, "UTF-8"));

//Execute and get the response.
HttpResponse response = httpclient.execute(httppost);
HttpEntity entity = response.getEntity();

if (entity != null) {
    try (InputStream instream = entity.getContent()) {
        // do something useful
    }
}
```

### Python – Book information retrieval
```python
import requests

r = requests.post(
    'http://34.65.4.90:3000/get_information',
    data={
        'request': 'love ministry duty',
        'book': '1984'
    })

print(r.status_code, r.reason)
print(r.json())
```

### C# – Semantic similarity
```csharp
using System.Net.Http;

private static readonly HttpClient client = new HttpClient();

var values = new Dictionary<string, string>
{
    {
    'request': 'love ministry duty',
    'book': '1984'
    }
};

var content = new FormUrlEncodedContent(values);
var response = await client.PostAsync("http://34.65.4.90:3000/get_information", content);
var responseString = await response.Content.ReadAsStringAsync();
```
