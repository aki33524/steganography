# steganography

This software hides message in png image file.

# Usage

```python
key = b'passphrase'

message_filename = 'data/embedded'
extracted_filename = 'data/extracted'
cover_filename 	= 'img/cover.png'
embedded_filename = 'img/coverd.png'

embed(key, cover_filename, message_filename, embedded_filename)
extract(key, embedded_filename, extracted_filename)

with open(message_filename, 'rb') as f:
  message = f.read()

with open(extracted_filename, 'rb') as f:
  extracted = f.read()

assert message == extracted
```

This is the coverwork image.
![cover.png](https://github.com/aki33524/steganography/blob/master/img/cover.png)

This is the message embedded image.
![coverd.png](https://github.com/aki33524/steganography/blob/master/img/coverd.png)

If message is short, probably you cannot distinguish these two image.
