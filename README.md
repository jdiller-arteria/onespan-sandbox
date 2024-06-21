# To start
`cp credentials.ini.example credentials.ini`

_Add valid onespan credentials to_ `credentials.ini`

`docker build --tag onespan-sandbox .`

`docker run -d -p 3000:5000 onespan-sandbox`

visit `http://localhost:3000`
