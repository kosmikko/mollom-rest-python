# Python GAE wrapper for Mollom REST API

Provides starting point for using [Mollom REST API](http://mollom.com/api/rest). 

Requires:

* [python-oauth](https://github.com/nshah/python-oauth)

Example of usage:

```python
mollom = request.MollomRequest()
print mollom.api_request('content',
                          http_method='POST',
                          post_data={'postBody': 'spam spam spam',
                                     'postTitle': 'ham ham ham',
                                     'checks': ["spam", "profanity"]
                          })
```

NB: I'm unlikely to maintain this any further. Feel free to fork it and make it better.